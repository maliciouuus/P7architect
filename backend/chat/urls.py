"""Routes HTTP de l'application tchat (vues HTML)."""

from django.urls import path

from . import views

urlpatterns = [
    # GET /chat/ → liste des salons disponibles
    path("", views.index, name="chat-index"),

    # GET /chat/<room_name>/ → interface du salon de tchat
    # La connexion WebSocket est gérée côté JS dans le template
    path("<str:room_name>/", views.room, name="chat-room"),
]
