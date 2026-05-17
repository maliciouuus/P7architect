#!/bin/sh
set -e

echo "==> Migrations..."
python3 manage.py migrate --no-input

echo "==> Initialisation des données de demo..."
python3 manage.py shell << 'PYEOF'
from django.contrib.auth.models import User
from chat.models import Room, Message

# Compte administrateur
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin1234')
    print("  Superuser cree : admin / admin1234")

# Compte agent support (pour tester le WebSocket a deux)
if not User.objects.filter(username='agent').exists():
    User.objects.create_user('agent', 'agent@example.com', 'agent1234')
    print("  Compte cree : agent / agent1234")

# Room de demonstration
if not Room.objects.filter(name='support-demo').exists():
    Room.objects.create(name='support-demo')
    print("  Room creee : support-demo")

# Messages de demo
room = Room.objects.get(name='support-demo')
if not Message.objects.filter(room=room).exists():
    admin = User.objects.get(username='admin')
    agent = User.objects.get(username='agent')
    Message.objects.create(room=room, author=admin, content="Bonjour, j'ai un probleme avec ma reservation #4521.")
    Message.objects.create(room=room, author=agent, content="Bonjour ! Je regarde ca immediatement.")
    Message.objects.create(room=room, author=admin, content="Merci beaucoup !")
    print("  Messages de demo crees")

print("==> Initialisation terminee")
PYEOF

echo "==> Demarrage de Daphne..."
exec daphne -b 0.0.0.0 -p 8000 config.asgi:application
