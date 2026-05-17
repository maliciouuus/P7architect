"""Routes de l'API REST de l'application tchat."""

from django.urls import path

from . import views

urlpatterns = [
    # GET  /api/chat/rooms/       → liste toutes les rooms
    # POST /api/chat/rooms/       → crée une nouvelle room
    path("rooms/", views.RoomListCreateView.as_view(), name="api-room-list"),

    # GET /api/chat/rooms/<room_name>/messages/ → liste les messages d'une room
    path(
        "rooms/<str:room_name>/messages/",
        views.MessageListView.as_view(),
        name="api-message-list",
    ),
]
