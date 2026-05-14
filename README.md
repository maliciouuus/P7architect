# Your Car Your Way — PoC Tchat

Preuve de concept de la fonctionnalité de tchat temps réel, développée dans le cadre du projet d'architecture P7 (OpenClassrooms).

## Contexte

Cette PoC démontre la faisabilité du tchat en temps réel retenu dans la proposition d'architecture. Elle se limite volontairement à cette seule fonctionnalité et ne constitue pas une application complète.

## Stack technique

| Composant | Technologie | Rôle |
|---|---|---|
| Backend | Django 4.2 | Framework web principal |
| Temps réel | Django Channels 4 + Daphne | Gestion des WebSockets |
| Broker de messages | Redis | Channel layer (diffusion entre workers) |
| API REST | Django REST Framework | Exposition des endpoints JSON |
| Base de données | SQLite (dev) / PostgreSQL (prod) | Persistance des messages |

## Architecture du tchat

```
Client (navigateur)
    │  WebSocket ws://host/ws/chat/<room>/
    ▼
Daphne (serveur ASGI)
    │
    ▼
Django Channels — ChatConsumer
    │  group_send / group_add
    ▼
Redis (Channel Layer)
    │  diffuse aux autres workers
    ▼
Tous les clients connectés à la room
```

## Structure du projet

```
P7architect/
├── backend/
│   ├── config/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── asgi.py          ← point d'entrée ASGI
│   ├── chat/
│   │   ├── models.py        ← Room, Message
│   │   ├── consumers.py     ← logique WebSocket
│   │   ├── routing.py       ← routes WebSocket
│   │   ├── views.py         ← vues HTML + API REST
│   │   ├── serializers.py   ← sérialisation DRF
│   │   └── templates/chat/
│   │       ├── index.html   ← liste des salons
│   │       └── room.html    ← interface du tchat
│   ├── manage.py
│   ├── requirements.txt
│   └── .env.example
├── docs/
│   ├── cahier_des_charges.md
│   └── proposition_architecture.md
└── frontend/               ← réservé pour l'intégration future
```

## Modèle de données

```
Room
 ├── id (PK)
 ├── name (unique)
 ├── created_at
 └── participants (M2M → User)

Message
 ├── id (PK)
 ├── room (FK → Room)
 ├── author (FK → User, nullable pour anonymisation RGPD)
 ├── content
 ├── sent_at
 └── is_read
```

## Lancer la PoC en local

**Prérequis** : Python 3.10+, Redis, Git

```bash
# 1. Cloner le dépôt
git clone <url-du-repo>
cd P7architect/backend

# 2. Créer et activer le virtualenv
python -m venv venv
source venv/bin/activate   # Linux/Mac
# venv\Scripts\activate    # Windows

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Configurer l'environnement
cp .env.example .env
# Éditer .env si besoin (clé secrète, URL Redis)

# 5. Appliquer les migrations
python manage.py migrate

# 6. Créer un superutilisateur
python manage.py createsuperuser

# 7. Lancer Redis (dans un terminal séparé)
redis-server

# 8. Lancer le serveur ASGI
daphne config.asgi:application
```

Accéder à l'interface : [http://localhost:8000/chat/](http://localhost:8000/chat/)

Pour créer des salons de tchat, aller dans l'admin : [http://localhost:8000/admin/](http://localhost:8000/admin/)

## Limites de la PoC

- Interface graphique minimaliste (l'objectif est la démonstration technique)
- Authentification via session Django (pas de JWT)
- SQLite utilisé pour simplifier le démarrage (PostgreSQL recommandé en production)
- Pas de tests automatisés dans le périmètre de cette PoC
