"""
Tests des serializers DRF.
On vérifie que la sérialisation JSON produit les bons champs
et que la désérialisation valide correctement les données.
"""

import pytest
from django.contrib.auth.models import User

from chat.models import Room, Message
from chat.serializers import RoomSerializer, MessageSerializer


@pytest.fixture
def user(db):
    return User.objects.create_user(username="alice", password="MotDePasse1")


@pytest.fixture
def room(db):
    return Room.objects.create(name="test-room")


@pytest.fixture
def message(db, room, user):
    return Message.objects.create(room=room, author=user, content="Hello !")


# ─── RoomSerializer ────────────────────────────────────────────

class TestRoomSerializer:

    def test_champs_presents(self, room):
        data = RoomSerializer(room).data
        assert "id" in data
        assert "name" in data
        assert "created_at" in data
        assert "message_count" in data
        assert "last_message" in data

    def test_message_count_zero(self, room):
        data = RoomSerializer(room).data
        assert data["message_count"] == 0

    def test_message_count_avec_messages(self, room, message):
        data = RoomSerializer(room).data
        assert data["message_count"] == 1

    def test_last_message_none_sans_messages(self, room):
        data = RoomSerializer(room).data
        assert data["last_message"] is None

    def test_last_message_avec_contenu(self, room, message):
        data = RoomSerializer(room).data
        assert data["last_message"] is not None
        assert "content" in data["last_message"]
        assert "sent_at" in data["last_message"]

    def test_creation_room_valide(self, db):
        serializer = RoomSerializer(data={"name": "nouvelle-room"})
        assert serializer.is_valid(), serializer.errors
        room = serializer.save()
        assert room.name == "nouvelle-room"

    def test_creation_room_name_vide(self, db):
        serializer = RoomSerializer(data={"name": ""})
        assert not serializer.is_valid()
        assert "name" in serializer.errors


# ─── MessageSerializer ──────────────────────────────────────────

class TestMessageSerializer:

    def test_champs_presents(self, message):
        data = MessageSerializer(message).data
        assert "id" in data
        assert "room" in data
        assert "author" in data
        assert "author_username" in data
        assert "content" in data
        assert "sent_at" in data
        assert "is_read" in data

    def test_author_username_correct(self, message):
        data = MessageSerializer(message).data
        assert data["author_username"] == "alice"

    def test_author_username_inconnu_si_null(self, db, room):
        msg = Message.objects.create(room=room, author=None, content="Anonymisé")
        data = MessageSerializer(msg).data
        assert data["author_username"] == "Inconnu"

    def test_is_read_false_par_defaut(self, message):
        data = MessageSerializer(message).data
        assert data["is_read"] is False

    def test_sent_at_est_une_chaine(self, message):
        """sent_at doit être sérialisé en ISO 8601."""
        data = MessageSerializer(message).data
        assert isinstance(data["sent_at"], str)
        assert "T" in data["sent_at"]
