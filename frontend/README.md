# Dossier frontend/

Ce dossier est actuellement vide. Il est réservé pour une future
intégration d'un framework JavaScript (React ou Vue.js) en Phase 3.

## Pourquoi ce dossier existe

L'architecture actuelle est un **monolithe Django** : les pages HTML
sont rendues côté serveur via les templates Django situés dans
`backend/chat/templates/`.

Ce dossier anticipe une évolution possible vers une architecture
découplée (SPA) sans avoir à restructurer le dépôt.

## Ce qui sera ici en Phase 3

- Application React ou Vue.js
- Connexion à l'API REST Django (DRF) via `http://localhost:8000/api/`
- Connexion WebSocket via `ws://localhost:8000/ws/chat/<room>/`

L'API REST et le routing WebSocket sont déjà prêts côté backend.
