from django.urls import path
from . import views

urlpatterns = [
    path("rooms/", views.RoomListCreateView.as_view(), name="api-room-list"),
    path("rooms/<str:room_name>/messages/", views.MessageListView.as_view(), name="api-message-list"),
]
