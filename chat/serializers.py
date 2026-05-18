"""Serializers DRF — convertissent les objets Django en JSON et inversement."""

from rest_framework import serializers

from .models import Message, Room


class MessageSerializer(serializers.ModelSerializer):
    """Sérialise un Message pour l'API REST."""

    # Champ calculé : retourne le username de l'auteur (ou "Inconnu" si NULL)
    # SerializerMethodField appelle automatiquement get_author_username()
    author_username = serializers.SerializerMethodField()

    class Meta:
        model = Message
        # Champs exposés dans la réponse JSON
        fields = [
            "id",
            "room",
            "author",
            "author_username",
            "content",
            "sent_at",
            "is_read",
        ]
        # Ces champs sont en lecture seule — ils ne peuvent pas être modifiés via l'API
        read_only_fields = ["id", "sent_at", "author"]

    def get_author_username(self, obj):
        """Retourne le nom d'utilisateur ou 'Inconnu' si le compte est supprimé."""
        return obj.author.username if obj.author else "Inconnu"


class RoomSerializer(serializers.ModelSerializer):
    """Sérialise une Room pour l'API REST."""

    # Compte le nombre de messages dans la room — calculé depuis la relation inverse
    message_count = serializers.IntegerField(
        source="messages.count",
        read_only=True,
    )

    # Dernier message envoyé dans la room (aperçu)
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = ["id", "name", "created_at", "message_count", "last_message"]
        read_only_fields = ["id", "created_at"]

    def get_last_message(self, obj):
        """Retourne un aperçu du dernier message ou None si la room est vide."""
        last = obj.messages.last()
        if last:
            return {
                "content": last.content[:80],        # tronqué à 80 caractères
                "sent_at": last.sent_at.isoformat(),  # format ISO 8601
            }
        return None
