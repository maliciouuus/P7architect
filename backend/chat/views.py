"""Vues HTTP et API REST pour l'application tchat."""

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from rest_framework import generics, permissions

from .models import Message, Room
from .serializers import MessageSerializer, RoomSerializer


# ── Vues HTML (interface de démonstration du PoC) ──────────────

@login_required  # redirige vers /accounts/login/ si non connecté
def index(request):
    """Affiche la liste de tous les salons de tchat disponibles."""
    rooms = Room.objects.all()  # récupère toutes les rooms depuis la base
    # passe les rooms au template HTML via le contexte
    return render(request, "chat/index.html", {"rooms": rooms})


@login_required
def room(request, room_name):
    """Affiche l'interface d'un salon de tchat.

    La connexion WebSocket est établie côté JavaScript dans le template.
    Si la room n'existe pas, Django retourne automatiquement une 404.
    """
    # get_object_or_404 : retourne la room ou lève une erreur HTTP 404
    room_obj = get_object_or_404(Room, name=room_name)
    return render(request, "chat/room.html", {"room": room_obj})


# ── Vues API REST (pour une future intégration front-end SPA) ──

class RoomListCreateView(generics.ListCreateAPIView):
    """Liste toutes les rooms (GET) ou en crée une nouvelle (POST).

    Requiert d'être authentifié (IsAuthenticated).
    """

    queryset = Room.objects.all()        # toutes les rooms de la base
    serializer_class = RoomSerializer   # convertit en JSON via RoomSerializer
    permission_classes = [permissions.IsAuthenticated]  # accès refusé si non connecté


class MessageListView(generics.ListAPIView):
    """Liste les messages d'une room spécifique (GET uniquement).

    URL : /api/chat/rooms/<room_name>/messages/
    Retourne 404 si la room n'existe pas.
    """

    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Filtre les messages selon le nom de la room dans l'URL."""
        room_name = self.kwargs["room_name"]  # extrait le paramètre de l'URL
        # vérifie que la room existe — lève 404 si elle n'existe pas
        get_object_or_404(Room, name=room_name)
        # retourne les messages de cette room avec l'auteur préchargé (optimisation)
        return (
            Message.objects.filter(room__name=room_name)
            .select_related("author")  # évite les requêtes SQL en cascade (N+1)
        )
