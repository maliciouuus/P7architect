from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework import generics, permissions
from .models import Room, Message
from .serializers import RoomSerializer, MessageSerializer


# --- Vues HTML (interface de démonstration du PoC) ---

@login_required
def index(request):
    """Liste des salons de tchat disponibles."""
    rooms = Room.objects.all()
    return render(request, "chat/index.html", {"rooms": rooms})


@login_required
def room(request, room_name):
    """Page d'un salon de tchat. La connexion WS est établie côté JS."""
    room_obj = get_object_or_404(Room, name=room_name)
    return render(request, "chat/room.html", {"room": room_obj})


# --- API REST (pour une future intégration front-end SPA) ---

class RoomListCreateView(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticated]


class MessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        room_name = self.kwargs["room_name"]
        return Message.objects.filter(room__name=room_name).select_related("author")
