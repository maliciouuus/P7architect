from django.contrib import admin
from .models import Room, Message


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ["name", "created_at"]
    search_fields = ["name"]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ["room", "author", "content_preview", "sent_at", "is_read"]
    list_filter = ["room", "is_read"]
    search_fields = ["content", "author__username"]

    def content_preview(self, obj):
        return obj.content[:60]
    content_preview.short_description = "Contenu"
