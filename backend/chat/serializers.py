from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Room, Message


class MessageSerializer(serializers.ModelSerializer):
    author_username = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ["id", "room", "author", "author_username", "content", "sent_at", "is_read"]
        read_only_fields = ["id", "sent_at", "author"]

    def get_author_username(self, obj):
        return obj.author.username if obj.author else "Inconnu"


class RoomSerializer(serializers.ModelSerializer):
    message_count = serializers.IntegerField(source="messages.count", read_only=True)
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = ["id", "name", "created_at", "message_count", "last_message"]
        read_only_fields = ["id", "created_at"]

    def get_last_message(self, obj):
        last = obj.messages.last()
        if last:
            return {
                "content": last.content[:80],
                "sent_at": last.sent_at.isoformat(),
            }
        return None
