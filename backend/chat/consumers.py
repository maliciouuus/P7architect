import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Room, Message


class ChatConsumer(AsyncWebsocketConsumer):
    """
    Consumer WebSocket gérant les connexions temps réel du tchat.

    Flux :
      1. Le client ouvre une connexion WS sur /ws/chat/<room_name>/
      2. Le consumer rejoint le groupe Redis correspondant à la room
      3. Chaque message reçu est persisté en base puis diffusé au groupe
      4. À la déconnexion, le consumer quitte le groupe
    """

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Vérifie que la room existe, sinon refuse la connexion
        room_exists = await self.get_room()
        if not room_exists:
            await self.close()
            return

        # Rejoindre le groupe Redis de la room
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # Envoyer l'historique des messages au client qui vient de se connecter
        history = await self.get_room_history()
        for msg in history:
            await self.send(text_data=json.dumps(msg))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        """Reçoit un message depuis le WebSocket client."""
        try:
            data = json.loads(text_data)
            content = data.get("message", "").strip()
        except (json.JSONDecodeError, KeyError):
            return

        if not content:
            return

        user = self.scope.get("user")
        if not user or not user.is_authenticated:
            await self.send(
                text_data=json.dumps({"error": "Authentification requise."})
            )
            return

        # Persistance en base de données
        message = await self.save_message(user, content)

        # Diffusion à tous les participants du groupe
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": content,
                "author": user.username,
                "sent_at": message["sent_at"],
                "message_id": message["id"],
            },
        )

    async def chat_message(self, event):
        """Handler appelé quand le groupe reçoit un message (type=chat_message)."""
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

    # --- Méthodes d'accès à la base de données (sync → async) ---

    @database_sync_to_async
    def get_room(self):
        try:
            self.room = Room.objects.get(name=self.room_name)
            return True
        except Room.DoesNotExist:
            return False

    @database_sync_to_async
    def get_room_history(self):
        """Retourne les 50 derniers messages de la room."""
        messages = (
            Message.objects.filter(room=self.room)
            .select_related("author")
            .order_by("-sent_at")[:50]
        )
        return [
            {
                "message": msg.content,
                "author": msg.author.username if msg.author else "Inconnu",
                "sent_at": msg.sent_at.isoformat(),
                "message_id": msg.id,
            }
            for msg in reversed(list(messages))
        ]

    @database_sync_to_async
    def save_message(self, user, content):
        msg = Message.objects.create(room=self.room, author=user, content=content)
        return {
            "id": msg.id,
            "sent_at": msg.sent_at.isoformat(),
        }
