"""
Tests des vues REST (API DRF).
On vérifie les permissions, les codes HTTP et le contenu des réponses.
"""

import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from chat.models import Room, Message


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username="alice",
        password="MotDePasse1",
        email="alice@example.com",
    )


@pytest.fixture
def room(db):
    return Room.objects.create(name="support-123")


@pytest.fixture
def client_auth(client, user):
    """Client HTTP connecté."""
    client.force_login(user)
    return client


# ─── API Rooms ──────────────────────────────────────────────────

class TestRoomListCreateView:

    def test_non_connecte_retourne_403(self, client):
        response = client.get("/api/chat/rooms/")
        assert response.status_code in (401, 403)

    def test_connecte_retourne_200(self, client_auth):
        response = client_auth.get("/api/chat/rooms/")
        assert response.status_code == 200

    def test_liste_vide(self, client_auth):
        response = client_auth.get("/api/chat/rooms/")
        assert response.json() == []

    def test_liste_avec_rooms(self, client_auth, room):
        response = client_auth.get("/api/chat/rooms/")
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "support-123"

    def test_creation_room(self, client_auth):
        response = client_auth.post(
            "/api/chat/rooms/",
            {"name": "nouvelle-room"},
            content_type="application/json",
        )
        assert response.status_code == 201
        assert response.json()["name"] == "nouvelle-room"

    def test_creation_room_name_existant(self, client_auth, room):
        response = client_auth.post(
            "/api/chat/rooms/",
            {"name": "support-123"},
            content_type="application/json",
        )
        assert response.status_code == 400


# ─── API Messages ───────────────────────────────────────────────

class TestMessageListView:

    def test_non_connecte_retourne_403(self, client, room):
        response = client.get(f"/api/chat/rooms/{room.name}/messages/")
        assert response.status_code in (401, 403)

    def test_messages_vides(self, client_auth, room):
        response = client_auth.get(f"/api/chat/rooms/{room.name}/messages/")
        assert response.status_code == 200
        assert response.json() == []

    def test_messages_avec_contenu(self, client_auth, room, user):
        Message.objects.create(room=room, author=user, content="Bonjour !")
        response = client_auth.get(f"/api/chat/rooms/{room.name}/messages/")
        data = response.json()
        assert len(data) == 1
        assert data[0]["content"] == "Bonjour !"
        assert data[0]["author_username"] == "alice"

    def test_room_inexistante_retourne_404(self, client_auth):
        response = client_auth.get("/api/chat/rooms/room-inexistante/messages/")
        assert response.status_code == 404

    def test_message_auteur_null(self, client_auth, room):
        """Message anonymisé (RGPD) : author_username = 'Inconnu'."""
        Message.objects.create(room=room, author=None, content="Anonymisé")
        response = client_auth.get(f"/api/chat/rooms/{room.name}/messages/")
        data = response.json()
        assert data[0]["author_username"] == "Inconnu"
