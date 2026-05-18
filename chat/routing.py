"""Routes WebSocket de l'application tchat.

Ce fichier est l'équivalent de urls.py mais pour les connexions
WebSocket. Il est chargé par config/asgi.py.
"""

from django.urls import re_path

from . import consumers

# Liste des routes WebSocket reconnues par Django Channels
websocket_urlpatterns = [
    # Route : ws://host/ws/chat/<room_name>/
    # [\w-]+ capture les lettres, chiffres, underscores ET tirets
    # (ex: "support-123" ou "room_test" sont tous les deux valides)
    re_path(
        r"ws/chat/(?P<room_name>[\w-]+)/$",
        consumers.ChatConsumer.as_asgi(),  # convertit le consumer en app ASGI
    ),
]
