"""
Tests des modèles Room et Message.
On vérifie la logique de données, les contraintes et les décisions
de conception (notamment la conformité RGPD sur l'anonymisation).
"""

import pytest
from django.contrib.auth.models import User
from django.db import IntegrityError

from chat.models import Room, Message


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username="alice",
        email="alice@example.com",
        password="MotDePasse1",
    )


@pytest.fixture
def autre_user(db):
    return User.objects.create_user(
        username="bob",
        email="bob@example.com",
        password="MotDePasse1",
    )


@pytest.fixture
def room(db):
    return Room.objects.create(name="support-001")


# ─── Tests Room ────────────────────────────────────────────────

class TestRoom:

    def test_creation_basique(self, room):
        assert room.id is not None
        assert room.name == "support-001"
        assert room.created_at is not None

    def test_str(self, room):
        assert str(room) == "support-001"

    def test_name_unique(self, db, room):
        """Deux rooms ne peuvent pas avoir le même nom."""
        with pytest.raises(IntegrityError):
            Room.objects.create(name="support-001")

    def test_participants_vide_par_defaut(self, room):
        assert room.participants.count() == 0

    def test_ajout_participants(self, room, user, autre_user):
        room.participants.add(user, autre_user)
        assert room.participants.count() == 2

    def test_un_user_peut_avoir_plusieurs_rooms(self, db, user):
        """Relation M2M : un utilisateur peut participer à N rooms."""
        r1 = Room.objects.create(name="room-a")
        r2 = Room.objects.create(name="room-b")
        r1.participants.add(user)
        r2.participants.add(user)
        assert user.rooms.count() == 2

    def test_ordering_par_date_desc(self, db):
        """Les rooms doivent être triées de la plus récente à la plus ancienne."""
        r1 = Room.objects.create(name="ancienne")
        r2 = Room.objects.create(name="recente")
        rooms = list(Room.objects.all())
        assert rooms[0] == r2
        assert rooms[1] == r1


# ─── Tests Message ─────────────────────────────────────────────

class TestMessage:

    def test_creation_basique(self, db, room, user):
        msg = Message.objects.create(
            room=room,
            author=user,
            content="Bonjour, j'ai un problème avec ma réservation.",
        )
        assert msg.id is not None
        assert msg.content == "Bonjour, j'ai un problème avec ma réservation."
        assert msg.is_read is False
        assert msg.sent_at is not None

    def test_str(self, db, room, user):
        msg = Message.objects.create(room=room, author=user, content="Test")
        assert "support-001" in str(msg)
        assert "alice" in str(msg)

    def test_ordering_chronologique(self, db, room, user):
        """Les messages doivent être triés du plus ancien au plus récent."""
        m1 = Message.objects.create(room=room, author=user, content="premier")
        m2 = Message.objects.create(room=room, author=user, content="deuxième")
        messages = list(Message.objects.filter(room=room))
        assert messages[0] == m1
        assert messages[1] == m2

    def test_is_read_false_par_defaut(self, db, room, user):
        msg = Message.objects.create(room=room, author=user, content="non lu")
        assert msg.is_read is False

    def test_marquer_comme_lu(self, db, room, user):
        msg = Message.objects.create(room=room, author=user, content="à lire")
        msg.is_read = True
        msg.save()
        msg.refresh_from_db()
        assert msg.is_read is True

    # ── Décision RGPD : author nullable ──────────────────────

    def test_message_sans_auteur(self, db, room):
        """Un message peut exister sans auteur (anonymisation RGPD)."""
        msg = Message.objects.create(room=room, author=None, content="Anonymisé")
        assert msg.author is None

    def test_anonymisation_a_la_suppression_compte(self, db, room, user):
        """
        Quand un utilisateur supprime son compte, ses messages doivent
        être conservés mais leur auteur mis à NULL (SET_NULL).
        C'est la décision RGPD centrale du modèle.
        """
        msg = Message.objects.create(room=room, author=user, content="Mon message")
        assert msg.author == user

        user.delete()

        msg.refresh_from_db()
        assert msg.author is None, (
            "Le message doit survivre à la suppression du compte "
            "(anonymisation RGPD via SET_NULL)"
        )
        assert msg.content == "Mon message", (
            "Le contenu du message doit être conservé après anonymisation"
        )

    def test_suppression_room_supprime_messages(self, db, room, user):
        """Quand une room est supprimée, ses messages le sont aussi (CASCADE)."""
        Message.objects.create(room=room, author=user, content="msg 1")
        Message.objects.create(room=room, author=user, content="msg 2")
        assert Message.objects.filter(room=room).count() == 2

        room.delete()

        assert Message.objects.count() == 0

    def test_plusieurs_messages_par_room(self, db, room, user, autre_user):
        Message.objects.create(room=room, author=user, content="Bonjour")
        Message.objects.create(room=room, author=autre_user, content="Bonjour aussi")
        assert Message.objects.filter(room=room).count() == 2

    def test_contenu_long(self, db, room, user):
        """Un message peut contenir jusqu'à 2000 caractères."""
        contenu = "a" * 2000
        msg = Message.objects.create(room=room, author=user, content=contenu)
        assert len(msg.content) == 2000
