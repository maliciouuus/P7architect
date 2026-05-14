# Proposition d'architecture — Application web centralisée
## Your Car Your Way

**Version** : 2.0  
**Date** : Avril 2026  
**Auteur** : Architecte logiciel — Your Car Your Way  
**Statut** : Document de référence validé  
**Destinataires** : Direction technique, équipes de développement, parties prenantes

---

## Avant-propos

Ce document présente l'architecture technique retenue pour la nouvelle application centralisée de Your Car Your Way. Il s'appuie sur le cahier des charges (document séparé) et constitue le **plan technique de référence** avant le début du développement.

Il répond à quatre questions fondamentales :
1. **Qu'est-ce qui existe aujourd'hui et quels sont ses problèmes ?** → Audit de l'existant
2. **Que doit faire techniquement le nouveau système ?** → Spécifications techniques
3. **Comment est organisée l'application ?** → Architecture applicative et diagrammes UML
4. **Quelles technologies utilise-t-on et pourquoi ?** → Choix technologiques argumentés

Chaque décision technique est **justifiée** et comparée à des alternatives crédibles. L'objectif est qu'un développeur, un chef de projet ou un manager puisse comprendre les choix retenus et les défendre.

---

## Sommaire

1. [Audit de l'existant](#1-audit-de-lexistant)
2. [Spécifications techniques](#2-spécifications-techniques)
3. [Architecture applicative](#3-architecture-applicative)
4. [Modèle de données](#4-modèle-de-données)
5. [Choix technologiques argumentés](#5-choix-technologiques-argumentés)
6. [Diagrammes UML](#6-diagrammes-uml)
7. [Synthèse des décisions](#7-synthèse-des-décisions)

---

## 1. Audit de l'existant

### 1.1 Qu'est-ce qu'un audit technique et à quoi sert-il ?

Un **audit technique** est une évaluation objective d'un système informatique existant. Il ne s'agit pas de critiquer les équipes qui l'ont développé — les choix du passé étaient souvent justifiés à leur époque. Il s'agit de comprendre ce qui fonctionne, ce qui pose problème, et pourquoi.

L'audit sert à :
- Éviter de répéter les erreurs du passé dans le nouveau système.
- Identifier les points forts à conserver ou s'inspirer.
- Justifier objectivement la décision de refaire l'application.

### 1.2 Critères d'évaluation retenus

Pour être rigoureux, l'audit s'appuie sur des **critères définis à l'avance**, pas sur des impressions subjectives.

| Critère | Définition | Pourquoi c'est important |
|---|---|---|
| **Maintenabilité** | Facilité à corriger des bugs, ajouter des fonctionnalités et faire évoluer le code sans tout casser | Un code difficile à maintenir ralentit l'équipe et coûte cher |
| **Performance** | Vitesse de réponse du système sous charge normale et en pic d'utilisation | Un site lent = clients qui partent |
| **Évolutivité** | Capacité à ajouter de nouvelles fonctionnalités ou à supporter plus d'utilisateurs | L'entreprise grandit : le système doit grandir avec elle |
| **Accessibilité** | Conformité aux normes WCAG 2.1 pour les personnes en situation de handicap | Obligation légale et enjeu éthique |
| **Cohérence fonctionnelle** | Homogénéité des fonctionnalités entre les différents marchés | Un client ne doit pas avoir une expérience dégradée selon son pays |
| **Sécurité** | Protection des données personnelles, conformité RGPD, résistance aux attaques | Obligation légale, confiance des clients |

### 1.3 Description des applications existantes

Your Car Your Way exploite actuellement **deux applications web distinctes** développées indépendamment :

#### Application Europe (marché historique)

- **Technologie backend** : PHP 7.x avec le framework Symfony
- **Base de données** : MySQL 5.7
- **Architecture** : Monolithique, sans API exposée
- **Langues** : Français, Anglais, Espagnol, Allemand
- **Fonctionnalités** : Inscription, connexion, recherche véhicules, réservation, gestion de compte, support par e-mail
- **Âge du code** : Certaines parties ont plus de 10 ans

#### Application Amérique du Nord

- **Technologie backend** : Node.js avec le framework Express
- **Base de données** : MongoDB (base de données NoSQL sans schéma fixe)
- **Architecture** : API REST partiellement exposée
- **Langues** : Anglais uniquement
- **Fonctionnalités** : Inscription, connexion, réservation basique — pas de réservation professionnelle, historique limité à 12 mois
- **Âge du code** : Plus récent (5 ans), mais rapidement développé sans vision long terme

#### Applications mobiles

- **Type** : WebView wrappers (des "coquilles" mobiles qui affichent simplement le site web existant)
- **Problème** : Pas une vraie application mobile. L'expérience sur mobile est médiocre.

### 1.4 Forces identifiées

Il est important d'identifier ce qui **fonctionne bien** dans l'existant, pour ne pas le perdre dans le nouveau système.

| Force | Application | Détail |
|---|---|---|
| Fonctionnalités métier matures | Europe | La réservation fonctionne, le catalogue est riche, les processus métier sont rodés |
| Support multilingue (4 langues) | Europe | Base de traduction existante réutilisable |
| API REST partiellement exposée | Amérique du Nord | Bonne pratique : découple le backend du frontend |
| Processus d'authentification établi | Les deux | Les utilisateurs ont déjà des comptes actifs |

### 1.5 Faiblesses identifiées

| Faiblesse | Critère impacté | Explication détaillée |
|---|---|---|
| **Deux codebases séparées** | Maintenabilité | Toute nouvelle fonctionnalité doit être développée deux fois. Un bug corrigé dans une application peut persister dans l'autre. Les coûts de maintenance doublent. |
| **Aucun compte unique cross-marchés** | Cohérence fonctionnelle | Un client européen qui loue au Canada doit créer un second compte. Il ne peut pas accéder à ses réservations européennes depuis l'application nord-américaine. |
| **Technologies hétérogènes** | Maintenabilité | PHP sur un serveur, Node.js sur un autre. Il faut des développeurs compétents dans les deux langages. Le recrutement est plus complexe et coûteux. |
| **MongoDB sans schéma strict** | Maintenabilité | Dans MongoDB, on peut sauvegarder n'importe quelle structure sans contrainte. En pratique, des champs ont des noms différents selon l'époque à laquelle ils ont été créés, rendant les requêtes instables. |
| **Absence totale de tchat** | Évolutivité | Le support client repose entièrement sur l'e-mail (délais 24-48h) et le téléphone. C'est un facteur de frustration identifié par les équipes terrain. |
| **Aucun audit d'accessibilité documenté** | Accessibilité | Aucune des deux applications n'a été testée pour la conformité WCAG. Les personnes en situation de handicap sont partiellement ou totalement exclues. |
| **Pas de logs centralisés** | Sécurité | Sans log d'audit centralisé, il est difficile de détecter une intrusion, de retracer une action frauduleuse ou de prouver la conformité RGPD. |
| **Pas d'API exposée (Europe)** | Évolutivité | L'application européenne est un monolithe fermé. Impossible de la connecter à une future application mobile native sans refonte complète. |
| **PHP 7.x en fin de vie** | Maintenabilité | PHP 7.x n'est plus maintenu par la communauté depuis décembre 2022. Aucun correctif de sécurité n'est plus publié. |

### 1.6 Conclusion de l'audit

L'audit révèle que l'existant remplit son rôle fonctionnel minimal (les réservations sont possibles), mais accumule une **dette technique significative** :

- **Maintenabilité** : ❌ Non satisfaisante. Deux codebases, deux technologies, une partie du code en fin de vie.
- **Performance** : ⚠️ Acceptable mais non mesurée. Aucun indicateur de performance documenté.
- **Évolutivité** : ❌ Faible. Les architectures fermées (pas d'API Europe) empêchent l'innovation.
- **Accessibilité** : ❌ Non conforme. Aucun audit, risque légal avéré.
- **Cohérence fonctionnelle** : ❌ Insuffisante. Expérience client très différente selon le marché.
- **Sécurité** : ⚠️ Partielle. Authentification en place, mais logs insuffisants et PHP en fin de vie.

**La décision de concevoir une nouvelle application centralisée est techniquement justifiée et nécessaire.** Continuer à maintenir l'existant représenterait un risque croissant (sécurité, légal, coûts) sans améliorer l'expérience client.

---

## 2. Spécifications techniques

### 2.1 Qu'est-ce qu'une spécification technique ?

Une spécification technique traduit les besoins fonctionnels (décrits dans le cahier des charges) en **exigences mesurables** pour les équipes de développement et d'infrastructure. Contrairement au cahier des charges qui dit "quoi", les spécifications techniques commencent à dire "avec quelles contraintes".

### 2.2 Contraintes héritées de l'existant

| Contrainte | Explication | Impact sur le projet |
|---|---|---|
| **Migration progressive** | L'application Europe ne peut pas être coupée du jour au lendemain. Des milliers de clients l'utilisent. | Le nouveau système doit pouvoir coexister avec l'ancien pendant 6 à 12 mois de transition |
| **Migration des données** | Les clients existants, leurs réservations et leur historique doivent être transférés dans le nouveau système | Un plan de migration de données (ETL) est nécessaire — hors périmètre de la PoC mais à planifier |
| **Continuité de service** | Aucune interruption de service de plus de 4 heures ne peut être planifiée | Nécessite une stratégie de déploiement "zéro downtime" |

### 2.3 Exigences non fonctionnelles techniques

Ces exigences sont **mesurables** et **testables**. Elles constituent les critères de validation du système en production.

| Exigence | Valeur cible | Comment la mesurer |
|---|---|---|
| **Temps de réponse HTTP** | < 2 secondes (95e percentile) | Tests de charge avec Locust ou k6 |
| **Latence WebSocket (tchat)** | < 500 millisecondes | Mesure du round-trip time en test |
| **Disponibilité mensuelle** | ≥ 99,5 % (= max 3h30 d'indisponibilité/mois) | Monitoring avec Uptime Robot ou Datadog |
| **Conformité accessibilité** | WCAG 2.1 niveau AA | Audit avec Axe DevTools, tests manuels avec NVDA |
| **Conformité RGPD** | Droit d'accès, rectification, effacement, portabilité | Revue juridique + tests des fonctionnalités RGPD |
| **Langues supportées** | Français, Anglais, Espagnol | Tests de non-régression des traductions |
| **Navigateurs supportés** | 2 dernières versions de Chrome, Firefox, Safari, Edge | Tests cross-browser avec BrowserStack |
| **Sécurité** | OWASP Top 10 couvert | Audit de sécurité (pentest léger) avant mise en production |

### 2.4 Contraintes de déploiement

| Contrainte | Décision retenue | Justification |
|---|---|---|
| **Hébergement** | Cloud (AWS ou GCP) | Flexibilité, scalabilité, pas d'infrastructure physique à maintenir |
| **Conteneurisation** | Docker recommandé | Reproductibilité des environnements (dev = recette = prod) |
| **Environnements** | Développement → Recette → Production | Permet de tester avant de déployer en production |
| **Chiffrement** | HTTPS et WSS obligatoires en production | Exigence RGPD et bonne pratique de sécurité universelle |
| **Sauvegardes** | Sauvegarde automatique quotidienne de la base de données | Conservation 7 jours minimum |

---

## 3. Architecture applicative

### 3.1 Qu'est-ce qu'une architecture logicielle ?

L'architecture logicielle, c'est la **façon d'organiser un système informatique** : comment les différentes parties sont découpées, comment elles communiquent entre elles, et comment elles sont déployées. C'est un plan directeur, comme les plans d'un architecte avant de construire un bâtiment.

Une mauvaise architecture crée des problèmes au fur et à mesure que le logiciel grossit. Une bonne architecture facilite la maintenance, les évolutions et le travail en équipe.

### 3.2 Les modèles d'architecture comparés

Avant de choisir une architecture, il faut comparer les options disponibles.

#### Option A — Architecture microservices

**Principe** : L'application est découpée en dizaines de petits services indépendants, chacun avec sa propre base de données et son propre déploiement.

**Avantages** :
- Chaque service peut être mis à jour indépendamment.
- Chaque service peut être mis à l'échelle indépendamment selon la charge.
- Une panne d'un service n'affecte pas les autres.

**Inconvénients** :
- Complexité opérationnelle très élevée (orchestration avec Kubernetes, monitoring de chaque service, gestion de la communication inter-services).
- Nécessite une équipe DevOps dédiée et expérimentée.
- Les transactions qui touchent plusieurs services sont complexes à gérer.
- Coût infrastructure plus élevé.

**Verdict pour ce projet** : ❌ Surdimensionné. Your Car Your Way n'est pas Amazon. Pour une équipe de taille moyenne et un budget contraint, les microservices ajoutent de la complexité sans bénéfice proportionnel.

#### Option B — Architecture serverless

**Principe** : Le code est découpé en fonctions exécutées à la demande sur l'infrastructure d'un cloud provider (AWS Lambda, Google Cloud Functions). Pas de serveur à gérer.

**Avantages** :
- Pas d'infrastructure à gérer.
- Paiement à l'usage (intéressant si le trafic est faible ou très variable).

**Inconvénients** :
- **Vendor lock-in** : fort couplage avec le cloud provider choisi.
- Gestion du tchat temps réel (WebSocket) très complexe en serverless.
- "Cold start" : un temps de démarrage (quelques secondes) si la fonction n'a pas été appelée récemment.
- Difficile à tester localement.

**Verdict pour ce projet** : ❌ Écarté. La fonctionnalité de tchat temps réel (WebSocket) est particulièrement difficile à implémenter en serverless. Le risque de vendor lock-in est trop élevé.

#### Option C — Monolithe modulaire (RETENU) ✅

**Principe** : L'application est un seul système déployé ensemble, mais organisé en **modules clairement séparés** (comptes, véhicules, réservations, tchat). Chaque module a ses propres responsabilités.

**Avantages** :
- Déploiement simple (un seul artifact).
- Cohérence des données facilitée (une seule base de données).
- Transactions simples entre modules.
- Équipe unique, outillage unifié.
- Scalabilité horizontale possible (plusieurs instances du même monolithe derrière un load balancer).

**Inconvénients** :
- Scalabilité moins granulaire qu'avec les microservices (on scale tout ou rien).
- Si un bug plante le processus, tout tombe (mitigation : plusieurs instances + monitoring).

**Verdict pour ce projet** : ✅ Retenu. Le monolithe modulaire est le meilleur compromis pour la taille de l'équipe, la complexité du projet et les contraintes budgétaires. Il peut évoluer vers des microservices dans 3 à 5 ans si la croissance le justifie.

### 3.3 Le modèle d'architecture en couches

À l'intérieur du monolithe modulaire, l'organisation interne suit une **architecture en couches** (layered architecture), augmentée d'une **couche événementielle** pour le tchat.

#### Les couches de l'application

```
┌─────────────────────────────────────────────────────┐
│         COUCHE PRÉSENTATION                         │
│  Templates HTML + API REST + WebSocket              │
│  Ce que l'utilisateur voit et avec quoi il interagit│
├─────────────────────────────────────────────────────┤
│         COUCHE LOGIQUE MÉTIER                       │
│  Apps Django : accounts, vehicles,                  │
│  reservations, chat                                 │
│  Les règles de l'entreprise (ex : annulation -48h)  │
├─────────────────────────────────────────────────────┤
│         COUCHE DONNÉES                              │
│  ORM Django + PostgreSQL                            │
│  Stockage et récupération des informations          │
└─────────────────────────────────────────────────────┘
```

**Pourquoi des couches ?**

Imaginez un restaurant : le serveur (couche présentation) prend la commande, la transmet au chef (couche métier) qui applique les recettes, et le garde-manger (couche données) stocke les ingrédients. Si on change le menu (règle métier), on ne touche pas à la façon dont les ingrédients sont stockés. Cette séparation rend le système plus facile à maintenir et à faire évoluer.

#### La couche événementielle (tchat temps réel)

Le tchat nécessite une technologie supplémentaire : les **WebSockets**. Contrairement au HTTP classique (le client pose une question, le serveur répond, la connexion est fermée), le WebSocket maintient une **connexion permanente** entre le navigateur et le serveur, permettant des échanges bidirectionnels instantanés.

> **Analogie** : HTTP, c'est comme envoyer une lettre et attendre la réponse par courrier. WebSocket, c'est comme un appel téléphonique : la ligne reste ouverte et les deux parties peuvent parler quand elles le souhaitent.

### 3.4 Vue d'ensemble de l'architecture complète

```
┌──────────────────────────────────────────────────────────┐
│                 CLIENT (Navigateur web)                  │
│  HTML / CSS / JavaScript                                 │
│  Connexion HTTP pour les pages                           │
│  Connexion WebSocket pour le tchat (persistante)         │
└──────────┬───────────────────────────┬───────────────────┘
           │ HTTPS                     │ WSS (WebSocket Sécurisé)
           ▼                           ▼
┌──────────────────────────────────────────────────────────┐
│                  Nginx (Reverse Proxy)                   │
│  Reçoit toutes les connexions entrantes                  │
│  Gère le chiffrement TLS (HTTPS/WSS)                    │
│  Met en cache les fichiers statiques (images, CSS, JS)   │
│  Transmet les requêtes à Daphne                          │
└──────────────────────────┬───────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────┐
│                Daphne (Serveur ASGI)                     │
│  Remplace Gunicorn : supporte HTTP ET WebSocket          │
│  ┌─────────────────────┐  ┌────────────────────────────┐ │
│  │   Django (HTTP)     │  │  Django Channels (WS)      │ │
│  │  Vues HTML          │  │  ChatConsumer              │ │
│  │  API REST (DRF)     │  │  Gère les connexions WS    │ │
│  │  Authentification   │  │  Reçoit/envoie les msgs    │ │
│  │  Admin back-office  │  └──────────────┬─────────────┘ │
│  └──────────┬──────────┘                 │               │
└─────────────┼─────────────────────────── │───────────────┘
              │                             │ group_send / group_add
              │                             ▼
              │              ┌──────────────────────────────┐
              │              │     Redis (Channel Layer)    │
              │              │  File de messages WebSocket  │
              │              │  Permet d'avoir plusieurs    │
              │              │  workers Daphne en parallèle │
              │              └──────────────────────────────┘
              │
              ▼
┌──────────────────────────────────────────────────────────┐
│                    PostgreSQL                            │
│  Base de données relationnelle unique                   │
│  Stocke : Users, Rooms, Messages, Vehicles,             │
│  Agencies, Reservations                                 │
└──────────────────────────────────────────────────────────┘
```

### 3.5 Rôle de chaque composant

| Composant | Rôle | Analogie |
|---|---|---|
| **Nginx** | Reçoit toutes les connexions, gère le chiffrement, distribue la charge | Le portier d'un immeuble qui oriente les visiteurs |
| **Daphne** | Exécute le code Django, traite les requêtes HTTP et WebSocket | Les employés de bureau qui traitent les demandes |
| **Django** | Framework applicatif : gère la logique métier, les vues, l'authentification | Le système de règles de l'entreprise |
| **Django Channels** | Extension de Django qui gère les connexions WebSocket du tchat | Le téléphoniste qui gère les appels en cours |
| **Redis** | File d'attente de messages pour synchroniser les workers du tchat | Le standard téléphonique central |
| **PostgreSQL** | Base de données relationnelle qui stocke toutes les données | L'armoire à dossiers de l'entreprise |

---

## 4. Modèle de données

### 4.1 Qu'est-ce qu'un modèle de données ?

Le modèle de données décrit **quelles informations** l'application stocke, **comment elles sont organisées** et **comment elles sont reliées entre elles**. C'est l'équivalent du plan d'une bibliothèque : quelles étagères existent, quels livres y sont rangés, et comment retrouver un livre.

En base de données relationnelle (PostgreSQL), les données sont organisées en **tables** (comme des feuilles de calcul). Les tables sont reliées entre elles par des **clés étrangères** (Foreign Keys).

### 4.2 Les entités du système

#### Entité User (Utilisateur)

Représente tout compte dans le système : client, agent support, administrateur. On utilise le **modèle User intégré de Django** comme base, ce qui évite de réécrire toute la gestion de l'authentification.

| Champ | Type | Description |
|---|---|---|
| id | Entier (PK) | Identifiant unique auto-incrémenté |
| email | Texte (unique) | Adresse e-mail, sert d'identifiant de connexion |
| first_name | Texte | Prénom |
| last_name | Texte | Nom de famille |
| language | Texte | Langue préférée (fr, en, es) |
| country | Texte | Pays de résidence |
| is_active | Booléen | Compte actif ou désactivé |
| is_staff | Booléen | True = accès au back-office admin |
| date_joined | Date/Heure | Date de création du compte |

#### Entité Room (Salon de tchat)

Représente une conversation de support entre un client et un ou plusieurs agents.

| Champ | Type | Description |
|---|---|---|
| id | Entier (PK) | Identifiant unique |
| name | Texte (unique) | Identifiant textuel de la room (ex: "support-client-456") |
| created_at | Date/Heure | Date de création |
| participants | Relation M2M → User | Utilisateurs autorisés à accéder à cette room |

**Pourquoi `participants` en Many-to-Many ?** Une room peut avoir plusieurs participants (le client + potentiellement plusieurs agents qui ont repris le dossier). Un utilisateur peut participer à plusieurs rooms (un agent gère plusieurs conversations). La relation Many-to-Many représente exactement cette réalité.

#### Entité Message

Représente un message envoyé dans une room.

| Champ | Type | Description | Décision de conception |
|---|---|---|---|
| id | Entier (PK) | Identifiant unique | — |
| room | FK → Room | Room à laquelle appartient le message | CASCADE : si la room est supprimée, les messages le sont aussi |
| author | FK → User (nullable) | Auteur du message | **SET_NULL** : si le compte est supprimé, le message est conservé mais l'auteur devient NULL (conformité RGPD) |
| content | Texte | Contenu du message | Limité à 2000 caractères (validation Django) |
| sent_at | Date/Heure | Horodatage d'envoi | Auto-généré à la création |
| is_read | Booléen | Message lu par le destinataire | Permet l'indicateur "Lu" dans l'interface |

**Décision RGPD sur `author` nullable** : Quand un client supprime son compte, on ne peut pas supprimer ses messages (l'historique de la conversation reste utile pour le support). On met donc le champ `author` à `NULL` : le message reste, mais son auteur est anonymisé ("Utilisateur supprimé" dans l'affichage).

#### Entité Vehicle (Véhicule)

| Champ | Type | Description |
|---|---|---|
| id | Entier (PK) | Identifiant unique |
| brand | Texte | Marque (Renault, Peugeot, Ford...) |
| model | Texte | Modèle (Clio, 308, Focus...) |
| year | Entier | Année du véhicule |
| category | Texte | Citadine, Berline, SUV, Utilitaire... |
| seats | Entier | Nombre de places |
| transmission | Texte | Manuelle ou Automatique |
| fuel | Texte | Essence, Diesel, Électrique, Hybride |
| price_per_day | Décimal | Prix de base par jour en euros |
| is_available | Booléen | Disponible à la réservation ou non |
| agency | FK → Agency | Agence de rattachement du véhicule |

#### Entité Agency (Agence)

| Champ | Type | Description |
|---|---|---|
| id | Entier (PK) | Identifiant unique |
| name | Texte | Nom de l'agence |
| address | Texte | Adresse postale complète |
| country | Texte | Pays |
| latitude | Décimal | Coordonnée GPS — latitude |
| longitude | Décimal | Coordonnée GPS — longitude |
| phone | Texte | Numéro de téléphone |
| is_active | Booléen | Agence ouverte ou temporairement fermée |

**Pourquoi `is_active` plutôt que supprimer l'agence ?** Si une agence ferme temporairement pour travaux, on ne peut pas la supprimer : des réservations passées y sont rattachées. `is_active = False` permet de la masquer aux clients tout en conservant l'historique.

#### Entité Reservation (Réservation)

| Champ | Type | Description |
|---|---|---|
| id | Entier (PK) | Identifiant unique |
| client | FK → User | Client qui a réservé |
| vehicle | FK → Vehicle | Véhicule réservé |
| start_date | Date | Date de prise en charge |
| end_date | Date | Date de restitution |
| pickup_agency | FK → Agency | Agence de départ |
| return_agency | FK → Agency | Agence de retour (peut être différente) |
| status | Texte (choices) | État de la réservation (voir ci-dessous) |
| total_price | Décimal | Prix total calculé à la confirmation |
| created_at | Date/Heure | Date de création de la réservation |

**Le cycle de vie d'une réservation (champ `status`)** :

```
pending (en attente de paiement)
    ↓
confirmed (confirmée)
    ↓                  ↘
completed (terminée)   cancelled (annulée)
```

### 4.3 Relations entre les entités (résumé)

| Relation | Type | Signification |
|---|---|---|
| User ↔ Room | Many-to-Many | Un utilisateur peut participer à plusieurs rooms, une room peut avoir plusieurs participants |
| Room → Message | One-to-Many | Une room contient plusieurs messages |
| User → Message | One-to-Many (nullable) | Un utilisateur peut envoyer plusieurs messages ; si supprimé, l'auteur devient NULL |
| Agency → Vehicle | One-to-Many | Une agence possède plusieurs véhicules |
| User → Reservation | One-to-Many | Un client peut avoir plusieurs réservations |
| Vehicle → Reservation | One-to-Many | Un véhicule peut avoir plusieurs réservations (passées et futures) |

---

## 5. Choix technologiques argumentés

Pour chaque composant de la stack technique, plusieurs options ont été comparées selon des critères objectifs avant de trancher.

### 5.1 Framework backend — Django 4.2 LTS

#### Les options comparées

| Critère | Django 4.2 | FastAPI | Node.js / Express |
|---|---|---|---|
| **Maturité** | Très élevée (20 ans d'existence) | Moyenne (créé en 2018) | Élevée (15 ans) |
| **ORM intégré** | ✅ Oui (ORM Django, très puissant) | ❌ Non (SQLAlchemy à configurer séparément) | ❌ Non (Sequelize ou Prisma à configurer) |
| **Interface d'administration** | ✅ Oui (auto-générée en quelques lignes) | ❌ Non (à développer de zéro) | ❌ Non |
| **Gestion WebSocket** | ✅ Via Django Channels (officiel) | ⚠️ Natif mais limité | ✅ Natif |
| **Authentification** | ✅ Intégrée (sessions, CSRF, passwords) | ❌ À configurer manuellement | ❌ Librairies tierces |
| **i18n (internationalisation)** | ✅ Support natif | ⚠️ Partiel | ❌ Bibliothèques tierces |
| **Communauté francophone** | Large | Petite | Moyenne |
| **Support LTS** | ✅ Jusqu'en avril 2026 (LTS) | ⚠️ Pas de LTS officiel | — |

**Décision : Django 4.2 LTS** ✅

Django offre une **productivité de développement très élevée** grâce à ses composants intégrés. Le back-office admin auto-généré représente à lui seul plusieurs semaines de développement économisées. Son ORM évite d'écrire du SQL à la main et réduit les risques d'erreurs. La version LTS (Long Term Support) garantit des correctifs de sécurité jusqu'en avril 2026.

> **Note sur Python** : Django est un framework Python. Python est le langage de programmation le plus populaire au monde (indice TIOBE 2024), avec une communauté immense et une documentation de qualité. Il est également utilisé pour les futures fonctionnalités d'analyse de données ou d'intelligence artificielle.

### 5.2 Temps réel (tchat) — Django Channels + Redis

#### Comment fonctionne le tchat en temps réel ?

En HTTP classique, le navigateur envoie une requête, le serveur répond, la connexion est fermée. Pour que le tchat soit "en temps réel", le serveur doit pouvoir **envoyer un message au navigateur sans que le navigateur l'ait demandé** (quand l'autre participant écrit).

Trois technologies permettent ça :

| Technologie | Fonctionnement | Adapté pour le tchat ? |
|---|---|---|
| **WebSocket** | Connexion bidirectionnelle persistante | ✅ Oui — la meilleure option |
| **Server-Sent Events (SSE)** | Connexion unidirectionnelle (serveur → client seulement) | ⚠️ Non — le client ne peut pas envoyer |
| **Long polling** | Le client redemande toutes les N secondes | ❌ Non — fausse impression de temps réel, charge serveur élevée |

#### Les options pour implémenter les WebSockets avec Django

| Option | Avantages | Inconvénients |
|---|---|---|
| **Django Channels + Redis** | Intégration native Django, équipe unique, Redis robuste | Redis à déployer séparément |
| **Socket.io (Node.js)** | Populaire, très documenté | Nécessite un second service Node.js — contredit l'objectif d'unification |
| **Pusher / Ably** | Service managé, zéro infra | Coût récurrent, vendor lock-in, données transitent chez un tiers |

**Décision : Django Channels 4 + Redis** ✅

Django Channels est l'extension officielle de Django pour les WebSockets. Elle transforme le serveur Django de WSGI (synchrone, pas de WebSocket) en **ASGI** (asynchrone, supporte WebSocket). Redis sert de **channel layer** : il permet à plusieurs workers Daphne de partager les messages WebSocket. Si un message arrive sur le worker 1, Redis le diffuse aussi au worker 2 où est connecté l'autre participant.

> **Pourquoi Redis ?** Redis est une base de données en mémoire ultra-rapide, conçue pour les cas d'usage où la vitesse prime. Elle est utilisée par Twitter, GitHub, Stack Overflow pour des cas similaires. Sa latence est de l'ordre de la microseconde.

### 5.3 Base de données — PostgreSQL 15

#### Les options comparées

| Critère | PostgreSQL 15 | MySQL 8 | MongoDB |
|---|---|---|---|
| **Type** | Relationnelle (SQL) | Relationnelle (SQL) | Documentaire (NoSQL) |
| **Schéma strict** | ✅ Oui | ✅ Oui | ❌ Non (problème identifié dans l'audit) |
| **Transactions ACID** | ✅ Complètes | ✅ Complètes | ⚠️ Partielles (depuis v4.0) |
| **Support Django ORM** | ✅ Natif, premium | ✅ Natif | ❌ Via djongo (non officiel, limité) |
| **Données JSON natives** | ✅ Type JSONB indexable | ⚠️ JSON limité | ✅ Natif |
| **Performances** | Excellentes | Bonnes | Bonnes (lecture) |
| **Extensions** | ✅ PostGIS (géospatial), Full-text search | ⚠️ Limitées | ⚠️ — |
| **Réputation industrie** | Standard de facto pour Django | Standard web généraliste | Adapté aux données non structurées |

**Décision : PostgreSQL 15** ✅

PostgreSQL est le choix logique pour plusieurs raisons :

1. **L'audit a montré les problèmes de MongoDB** : l'absence de schéma strict a créé des incohérences dans la base nord-américaine. PostgreSQL impose un schéma, ce qui garantit la qualité des données.
2. **Les réservations sont des données critiques** : ACID signifie que si une opération échoue à mi-chemin (ex : la réservation est créée mais l'e-mail n'est pas envoyé), la base revient à son état antérieur. Pas de données à moitié enregistrées.
3. **Extension PostGIS** : si la recherche d'agences par géolocalisation est ajoutée, PostgreSQL + PostGIS le gère nativement.

### 5.4 API REST — Django REST Framework (DRF)

**Option retenue : DRF 3.14** ✅ — il n'y a pas vraiment de concurrent sérieux dans l'écosystème Django.

DRF fournit en quelques lignes de code :
- La **sérialisation** des données (conversion Python → JSON et inversement)
- L'**authentification** (session, token, JWT selon le besoin)
- La **pagination** des résultats
- La **validation** des données entrantes
- La **documentation automatique** de l'API (via `drf-spectacular`)

> **GraphQL vs REST** : GraphQL est une alternative à REST permettant au client de spécifier exactement les données qu'il veut. C'est utile pour des APIs publiques complexes. Dans ce projet, l'API est interne et ses besoins sont bien définis — REST est plus simple, plus documenté et plus rapide à mettre en place.

### 5.5 Serveur ASGI — Daphne

**Contexte** : Django utilise historiquement **Gunicorn** comme serveur. Mais Gunicorn est un serveur WSGI (synchrone) qui **ne supporte pas les WebSockets**. Dès lors qu'on intègre Django Channels, il faut passer à un serveur ASGI.

**Option retenue : Daphne** ✅

Daphne est développé par la même équipe que Django Channels. Il est conçu exactement pour ce cas d'usage. En production, il est placé derrière **Nginx** qui gère le chiffrement TLS et le cache des fichiers statiques.

**Alternative évaluée : Uvicorn + Gunicorn**. Uvicorn est un serveur ASGI très performant, souvent utilisé avec FastAPI. Il fonctionne aussi avec Django Channels, mais nécessite une configuration plus complexe. Pour une équipe qui débute avec ASGI, Daphne est plus simple et mieux intégré.

---

## 6. Diagrammes UML

> Les diagrammes suivants ont été générés avec **PlantUML**, outil standard de l'industrie pour la modélisation UML.

### 6.1 Diagramme de classes — Modèle de données

Ce diagramme représente les entités de la base de données et leurs relations. C'est la vue "données" de l'application.

### 6.2 Diagramme de composants

Ce diagramme représente les modules logiciels de l'application (les apps Django) et leurs dépendances vers l'infrastructure externe. C'est la vue "organisation du code".

### 6.3 Diagramme de séquence — Envoi d'un message de tchat

Ce diagramme montre, dans l'ordre chronologique, les échanges entre les différents acteurs lors de l'envoi d'un message. C'est la vue "dynamique" du tchat.

**Lecture du diagramme** : chaque colonne verticale représente un acteur ou un composant. Les flèches horizontales représentent les échanges (messages, appels de fonctions, requêtes). Le temps s'écoule de haut en bas.

### 6.4 Diagramme de déploiement

Ce diagramme montre comment les composants logiciels sont déployés sur l'infrastructure physique (ou cloud). C'est la vue "infrastructure".

---

## 7. Synthèse des décisions

### 7.1 Tableau récapitulatif

| Décision | Choix retenu | Alternative principale écartée | Raison principale du choix |
|---|---|---|---|
| **Architecture globale** | Monolithe modulaire | Microservices | Complexité adaptée à la taille de l'équipe, évolutif vers microservices si besoin |
| **Framework backend** | Django 4.2 LTS | FastAPI | ORM intégré, admin auto-généré, authentification native, i18n, LTS |
| **Temps réel (tchat)** | Django Channels 4 + Redis | Socket.io (Node.js) | Intégration native Django, pas de second service à maintenir |
| **Base de données** | PostgreSQL 15 | MongoDB | Schéma strict, transactions ACID, support Django ORM natif |
| **Serveur applicatif** | Daphne (ASGI) | Gunicorn (WSGI) | Gunicorn ne supporte pas WebSocket |
| **API** | REST (Django REST Framework) | GraphQL | Standard, outillage mature, besoins bien définis |
| **Proxy / TLS** | Nginx | Apache | Performance, gestion du cache statique, configuration WebSocket |
| **Langage** | Python 3.11+ | PHP, JavaScript (Node) | Unification sur un seul langage, écosystème riche, futur IA/data |

### 7.2 Cohérence avec les exigences fonctionnelles

| Exigence fonctionnelle | Comment l'architecture y répond |
|---|---|
| Compte unique cross-marchés | Une seule base de données PostgreSQL, un seul modèle `User` |
| Tchat temps réel | Django Channels + WebSocket + Redis Channel Layer |
| Accessibilité WCAG 2.1 | Templates Django avec HTML sémantique, ARIA dans les templates tchat |
| Multilingue | Système i18n natif Django (fichiers .po) |
| RGPD — droit à l'effacement | Champ `author` nullable dans `Message` (SET_NULL), endpoint d'export |
| Performance < 2s | Nginx cache statiques, PostgreSQL indexé, Redis cache sessions |
| Back-office administrateur | Django Admin auto-généré, personnalisé avec `ModelAdmin` |
| API pour futures apps mobiles | Django REST Framework expose des endpoints JSON documentés |

### 7.3 Ce que cette architecture ne résout pas (honnêteté)

Toute architecture a des limites. Voici les points d'attention pour le futur :

| Limite | Quand ça devient un problème | Solution envisageable |
|---|---|---|
| Scalabilité du monolithe | Si le trafic dépasse 10 000 utilisateurs simultanés | Extraction en microservices des modules les plus sollicités |
| Base de données unique | En cas de volume de données très important (millions de messages) | Partitionnement des tables ou base séparée pour le tchat |
| Daphne en production | Pour des charges très élevées | Remplacer par Uvicorn + Gunicorn multi-worker |
| Pas de paiement | Dès que le paiement en ligne est requis | Intégration Stripe ou Adyen en phase 2 |
