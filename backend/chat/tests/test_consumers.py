"""Tests du ChatConsumer WebSocket.

WebsocketCommunicator simule un vrai navigateur sans
avoir besoin d'un serveur réseau réel.
"""

import pytest
from channels.db import database_sync_to_async
from channels.testing import WebsocketCommunicator
from django.contrib.auth.models import User

from chat.models import Message, Room
from config.asgi import application


# ── Fixtures (données réutilisables entre les tests) ───────────

@pytest.fixture
def user(db):
    """Crée un utilisateur de test en base."""
    return User.objects.create_user(
        username="alice",
        password="MotDePasse1",
    )


@pytest.fixture
def room(db):
    """Crée un salon de tchat de test en base."""
    return Room.objects.create(name="test-ws")


# ── Helpers asynchrones ────────────────────────────────────────

@database_sync_to_async
def get_message_count(room):
    """Compte les messages d'une room (version async pour les tests)."""
    return Message.objects.filter(room=room).count()


@database_sync_to_async
def get_last_message(room):
    """Retourne le dernier message d'une room (version async)."""
    return Message.objects.filter(room=room).order_by("-sent_at").first()


# ── Tests ──────────────────────────────────────────────────────

# django_db(transaction=True) est requis pour les tests async
# qui accèdent à la base de données avec database_sync_to_async
@pytest.mark.django_db(transaction=True)
class TestChatConsumer:
    """Tests du consumer WebSocket."""

    async def test_connexion_room_existante(self, room, user):
        """Un utilisateur connecté peut rejoindre une room existante."""

        # Crée un faux client WebSocket qui se connecte à l'URL de la room
        communicator = WebsocketCommunicator(
            application,                    # l'application ASGI complète
            f"/ws/chat/{room.name}/",       # URL de connexion
        )

        # Injecte l'utilisateur dans le scope (simule la session Django)
        communicator.scope["user"] = user

        # Tente la connexion — retourne (True, code) si acceptée
        connected, _ = await communicator.connect()
        assert connected, "La connexion WebSocket doit être acceptée"

        # Ferme proprement la connexion après le test
        await communicator.disconnect()

    async def test_connexion_room_inexistante(self, db, user):
        """La connexion doit être refusée si la room n'existe pas."""
        communicator = WebsocketCommunicator(
            application,
            "/ws/chat/room-qui-nexiste-pas/",
        )
        communicator.scope["user"] = user

        connected, _ = await communicator.connect()
        # Le consumer appelle self.close() si la room est introuvable
        assert not connected, "La connexion doit être refusée"

    async def test_reception_historique_a_la_connexion(self, room, user):
        """À la connexion, le client reçoit les messages existants."""

        # Crée un message en base AVANT la connexion
        await database_sync_to_async(Message.objects.create)(
            room=room,
            author=user,
            content="Message historique",
        )

        communicator = WebsocketCommunicator(
            application,
            f"/ws/chat/{room.name}/",
        )
        communicator.scope["user"] = user
        await communicator.connect()

        # Le premier message reçu doit être le message historique
        response = await communicator.receive_json_from()
        assert response["message"] == "Message historique"
        assert response["author"] == "alice"

        await communicator.disconnect()

    async def test_envoi_message_persiste_en_base(self, room, user):
        """Un message envoyé via WebSocket doit être sauvegardé en base."""
        communicator = WebsocketCommunicator(
            application,
            f"/ws/chat/{room.name}/",
        )
        communicator.scope["user"] = user
        await communicator.connect()

        # Envoie un message JSON au consumer (simule le navigateur)
        await communicator.send_json_to({"message": "Bonjour depuis le test !"})

        # Attend la réponse diffusée par le consumer
        response = await communicator.receive_json_from()
        assert response["message"] == "Bonjour depuis le test !"

        # Vérifie que le message a bien été sauvegardé en base PostgreSQL
        count = await get_message_count(room)
        assert count == 1

        await communicator.disconnect()

    async def test_message_vide_non_traite(self, room, user):
        """Un message vide ou composé d'espaces ne doit pas être persisté."""
        communicator = WebsocketCommunicator(
            application,
            f"/ws/chat/{room.name}/",
        )
        communicator.scope["user"] = user
        await communicator.connect()

        # Envoie un message composé uniquement d'espaces
        await communicator.send_json_to({"message": "   "})

        # receive_nothing() retourne True si aucun message n'est arrivé
        # (timeout court pour ne pas bloquer le test)
        assert await communicator.receive_nothing()

        # Vérifie qu'aucun message n'a été créé en base
        count = await get_message_count(room)
        assert count == 0

        await communicator.disconnect()

    async def test_message_contient_horodatage(self, room, user):
        """La réponse WebSocket doit contenir l'horodatage ISO 8601."""
        communicator = WebsocketCommunicator(
            application,
            f"/ws/chat/{room.name}/",
        )
        communicator.scope["user"] = user
        await communicator.connect()

        await communicator.send_json_to({"message": "Test horodatage"})
        response = await communicator.receive_json_from()

        # Vérifie la présence du champ sent_at au format ISO 8601 (contient "T")
        assert "sent_at" in response
        assert "T" in response["sent_at"]

        # Vérifie la présence de l'identifiant unique du message
        assert "message_id" in response

        await communicator.disconnect()

    async def test_user_non_connecte_refuse(self, room):
        """Un utilisateur non authentifié doit recevoir une erreur JSON."""
        from django.contrib.auth.models import AnonymousUser

        communicator = WebsocketCommunicator(
            application,
            f"/ws/chat/{room.name}/",
        )
        # AnonymousUser simule un utilisateur non connecté
        communicator.scope["user"] = AnonymousUser()
        await communicator.connect()

        # Envoie un message comme si l'utilisateur était connecté
        await communicator.send_json_to({"message": "Je suis anonyme"})

        # Le consumer doit retourner un JSON avec une clé "error"
        response = await communicator.receive_json_from()
        assert "error" in response

        await communicator.disconnect()
