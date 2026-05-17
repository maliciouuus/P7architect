"""Consumer WebSocket pour le tchat temps réel."""

import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import Message, Room


class ChatConsumer(AsyncWebsocketConsumer):
    """Gère une connexion WebSocket entre un client et le serveur.

    Cycle de vie :
      1. connect()  — le navigateur ouvre la connexion
      2. receive()  — un message arrive du navigateur
      3. disconnect() — le navigateur ferme la connexion

    Le channel layer Redis diffuse les messages à tous
    les participants connectés à la même room.
    """

    async def connect(self):
        """Appelée quand un navigateur ouvre la connexion WebSocket."""

        # Récupère le nom de la room depuis l'URL (/ws/chat/<room_name>/)
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]

        # Nom du groupe Redis qui regroupe tous les workers de cette room
        self.room_group_name = f"chat_{self.room_name}"

        # Vérifie que la room existe en base — refuse sinon
        room_exists = await self.get_room()
        if not room_exists:
            # close() ferme la connexion WS avec un code d'erreur
            await self.close()
            return

        # Ajoute ce worker au groupe Redis de la room
        # (tous les workers du groupe reçoivent les messages envoyés au groupe)
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,  # identifiant unique de ce worker
        )

        # Accepte officiellement la connexion WebSocket
        await self.accept()

        # Envoie les 50 derniers messages au client qui vient de se connecter
        history = await self.get_room_history()
        for msg in history:
            await self.send(text_data=json.dumps(msg))

    async def disconnect(self, close_code):
        """Appelée quand le navigateur ferme la connexion."""

        # Retire ce worker du groupe Redis — il ne recevra plus les messages
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )

    async def receive(self, text_data):
        """Appelée quand le navigateur envoie un message via WebSocket."""

        # Décode le JSON reçu : {"message": "Bonjour !"}
        try:
            data = json.loads(text_data)
            content = data.get("message", "").strip()
        except (json.JSONDecodeError, KeyError):
            # Message malformé — on ignore silencieusement
            return

        # Refuse les messages vides ou composés uniquement d'espaces
        if not content:
            return

        # Récupère l'utilisateur connecté depuis le scope (session Django)
        user = self.scope.get("user")
        if not user or not user.is_authenticated:
            # Envoie une erreur JSON au client et arrête le traitement
            await self.send(
                text_data=json.dumps({"error": "Authentification requise."})
            )
            return

        # Sauvegarde le message en base PostgreSQL
        message = await self.save_message(user, content)

        # Diffuse le message à TOUS les workers connectés à cette room via Redis
        # type="chat_message" indique quelle méthode handler appeler
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",   # → appelle self.chat_message()
                "message": content,
                "author": user.username,
                "sent_at": message["sent_at"],
                "message_id": message["id"],
            },
        )

    async def chat_message(self, event):
        """Handler Redis : reçoit un message du groupe et le transmet au navigateur.

        Cette méthode est appelée automatiquement par Channels
        quand le groupe Redis reçoit un event de type 'chat_message'.
        """

        # Envoie le message au navigateur sous forme de JSON
        await self.send(
            text_data=json.dumps(
                {
                    "message": event["message"],
                    "author": event["author"],
                    "sent_at": event["sent_at"],
                    "message_id": event["message_id"],
                }
            )
        )

    # ── Méthodes d'accès à la base de données ──────────────────
    # @database_sync_to_async convertit une fonction synchrone (ORM Django)
    # en fonction asynchrone utilisable avec await

    @database_sync_to_async
    def get_room(self):
        """Vérifie que la room existe. Stocke l'objet Room dans self.room."""
        try:
            # Cherche la room par son nom — lève DoesNotExist si absente
            self.room = Room.objects.get(name=self.room_name)
            return True
        except Room.DoesNotExist:
            return False

    @database_sync_to_async
    def get_room_history(self):
        """Retourne les 50 derniers messages de la room (ordre chronologique)."""

        # Requête optimisée : select_related évite les requêtes N+1 sur author
        messages = (
            Message.objects.filter(room=self.room)
            .select_related("author")
            .order_by("-sent_at")[:50]  # 50 plus récents en ordre décroissant
        )

        # reversed() remet dans l'ordre chronologique pour l'affichage
        return [
            {
                "message": msg.content,
                "author": msg.author.username if msg.author else "Inconnu",
                "sent_at": msg.sent_at.isoformat(),  # format ISO 8601
                "message_id": msg.id,
            }
            for msg in reversed(list(messages))
        ]

    @database_sync_to_async
    def save_message(self, user, content):
        """Sauvegarde un message en base et retourne son id et horodatage."""
        msg = Message.objects.create(
            room=self.room,
            author=user,
            content=content,
        )
        # Retourne un dict sérialisable (pas l'objet Django directement)
        return {
            "id": msg.id,
            "sent_at": msg.sent_at.isoformat(),
        }
