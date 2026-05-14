# Cahier des charges — Application web centralisée
## Your Car Your Way

**Version** : 2.0  
**Date** : Avril 2026  
**Auteur** : Architecte logiciel — Your Car Your Way  
**Statut** : Document consolidé — prêt pour validation  
**Destinataires** : Direction, équipes techniques, parties prenantes métier

---

## Avant-propos

Ce document constitue le cahier des charges complet de la nouvelle application web centralisée de Your Car Your Way. Il a été rédigé à partir de l'analyse des besoins métier existants, des retours des équipes terrain et des exigences réglementaires applicables (RGPD, WCAG/RGAA).

Son objectif est double :
- Servir de **référence contractuelle** entre les équipes métier et les équipes techniques.
- Garantir que **tous les profils d'utilisateurs**, y compris les personnes en situation de handicap, ont été pris en compte dès la conception.

Un cahier des charges n'est pas un manuel technique. Il décrit **ce que le système doit faire**, pas **comment il le fait**. Les choix techniques sont traités dans la proposition d'architecture (document séparé).

---

## Sommaire

1. [Contexte et enjeux du projet](#1-contexte-et-enjeux-du-projet)
2. [Objectifs du projet](#2-objectifs-du-projet)
3. [Périmètre du projet](#3-périmètre-du-projet)
4. [Profils utilisateurs (personas)](#4-profils-utilisateurs-personas)
5. [Considérations transverses](#5-considérations-transverses)
6. [Spécifications fonctionnelles — User Stories](#6-spécifications-fonctionnelles--user-stories)
7. [Priorisation MoSCoW](#7-priorisation-moscow)
8. [Contraintes et hypothèses](#8-contraintes-et-hypothèses)
9. [Glossaire](#9-glossaire)

---

## 1. Contexte et enjeux du projet

### 1.1 Qui est Your Car Your Way ?

Your Car Your Way est une entreprise de **location de voitures** fondée il y a plus de vingt ans. Elle est implantée en Europe depuis ses débuts et s'est récemment développée en **Amérique du Nord**. Elle compte plusieurs milliers de clients actifs et des dizaines d'agences réparties dans plusieurs pays.

Comme beaucoup d'entreprises qui ont grandi rapidement, Your Car Your Way a développé ses outils informatiques **pays par pays**, sans vision globale. Résultat : aujourd'hui, l'entreprise gère plusieurs applications web distinctes, chacune avec sa propre technologie, ses propres fonctionnalités et ses propres équipes de développement.

### 1.2 Pourquoi ce projet est-il nécessaire ?

#### Problème 1 — La complexité technique

Maintenir plusieurs applications séparées coûte cher et prend du temps. Quand une nouvelle fonctionnalité est développée pour le marché européen, elle doit être **redéveloppée de zéro** pour l'Amérique du Nord, avec des technologies différentes. Chaque bug corrigé dans une application doit être retrouvé et corrigé dans l'autre.

> **Analogie** : C'est comme si une chaîne de restaurants devait imprimer un menu différent pour chaque ville, avec des recettes différentes pour le même plat. La gestion devient vite un cauchemar.

#### Problème 2 — Les incohérences fonctionnelles

Un client européen qui loue une voiture en Europe peut accéder à son historique de réservations sur 24 mois. En revanche, s'il voyage au Canada et utilise l'application nord-américaine, il ne peut pas voir ses réservations européennes. Les deux applications ne se "parlent" pas.

Certaines fonctionnalités disponibles en Europe sont tout simplement absentes en Amérique du Nord, ce qui crée une **expérience utilisateur inégale et frustrante**.

#### Problème 3 — Les difficultés de maintenance

Chaque application a été développée avec des technologies différentes à des époques différentes. Certaines parties du code sont vieillissantes, peu documentées, et difficiles à modifier sans risquer de tout casser. Les équipes techniques passent plus de temps à "réparer" qu'à "innover".

#### Problème 4 — Les risques réglementaires

La réglementation européenne sur l'accessibilité du web (RGAA) et sur la protection des données (RGPD) impose des obligations légales. Les applications actuelles n'ont pas fait l'objet d'un audit d'accessibilité documenté, ce qui expose l'entreprise à des risques juridiques.

### 1.3 La solution envisagée

Your Car Your Way souhaite développer une **nouvelle application web unique**, centralisée, qui :
- Remplace progressivement toutes les applications existantes.
- Serve tous les marchés (Europe, Amérique du Nord, et futurs marchés).
- Soit accessible à tous les utilisateurs, y compris les personnes en situation de handicap.
- Respecte les réglementations en vigueur (RGPD, WCAG 2.1).
- Soit maintenable et évolutive sur le long terme.

---

## 2. Objectifs du projet

Les objectifs sont classés en deux catégories : **fonctionnels** (ce que l'application doit permettre de faire) et **non fonctionnels** (les qualités que l'application doit avoir).

### 2.1 Objectifs fonctionnels

| # | Objectif | Pourquoi c'est important |
|---|---|---|
| OF-1 | Permettre à tout client de créer un compte unique valable dans tous les pays | Aujourd'hui impossible — un client doit recréer un compte par pays |
| OF-2 | Permettre la recherche et la réservation de véhicules en ligne | Cœur de métier de l'entreprise |
| OF-3 | Offrir un tchat en temps réel entre le client et le support | Réduire les délais de réponse, améliorer la satisfaction client |
| OF-4 | Donner accès à l'historique complet des réservations | Fidéliser les clients, simplifier les litiges |
| OF-5 | Fournir un back-office aux équipes internes | Gérer véhicules, agences, réservations, utilisateurs |
| OF-6 | Supporter plusieurs langues et devises | Cohérence avec la présence internationale de l'entreprise |

### 2.2 Objectifs non fonctionnels

Les objectifs non fonctionnels définissent la **qualité** du système, pas ses fonctionnalités.

| # | Objectif | Valeur cible | Justification |
|---|---|---|---|
| ONF-1 | **Performance** : temps de réponse | < 2 secondes (95% des requêtes) | Au-delà, 40% des utilisateurs abandonnent (source : Google) |
| ONF-2 | **Disponibilité** | 99,5 % par mois (≈ 3h30 d'arrêt max/mois) | Service critique pour les voyageurs |
| ONF-3 | **Accessibilité** | WCAG 2.1 niveau AA minimum | Obligation légale (RGAA en France) |
| ONF-4 | **Sécurité des données** | Conformité RGPD (UE 2016/679) | Obligation légale sous peine d'amendes CNIL |
| ONF-5 | **Latence du tchat** | < 500 ms | Expérience de conversation fluide |
| ONF-6 | **Internationalisation** | Français, Anglais, Espagnol (extensible) | Marchés actuels + croissance future |
| ONF-7 | **Compatibilité navigateurs** | 2 dernières versions des navigateurs majeurs | Couvre 95%+ des utilisateurs |

---

## 3. Périmètre du projet

### 3.1 Ce qui est inclus dans ce projet

- Gestion des comptes utilisateurs (inscription, connexion, profil, suppression RGPD)
- Recherche de véhicules disponibles selon des critères
- Réservation de véhicules et gestion du cycle de vie (confirmation, annulation)
- Tchat en temps réel entre le client et le support
- Historique des réservations pour le client
- Back-office de gestion pour les administrateurs
- Support multilingue (FR, EN, ES)

### 3.2 Ce qui est explicitement exclu (hors périmètre)

- Le paiement en ligne (fera l'objet d'une phase ultérieure, intégration d'un prestataire de paiement comme Stripe)
- L'application mobile native (iOS / Android)
- La migration des données existantes (projet séparé)
- La gestion de la flotte (maintenance des véhicules, planning garage)

> **Pourquoi exclure le paiement ?** Le paiement en ligne est un sujet complexe avec des exigences de sécurité très spécifiques (norme PCI-DSS). L'intégrer dans ce périmètre risquerait de retarder l'ensemble du projet. Il sera traité dans une phase 2.

---

## 4. Profils utilisateurs (personas)

Un **persona** est une représentation fictive mais réaliste d'un type d'utilisateur. Définir des personas permet de concevoir l'application en se mettant à la place de chaque utilisateur, pas seulement du "cas standard".

### 4.1 Persona 1 — Le client particulier

**Prénom fictif** : Marc, 38 ans, cadre commercial  
**Situation** : Marc voyage fréquemment en Europe pour son travail. Il réserve des voitures depuis son téléphone ou son ordinateur, souvent en déplacement.

**Ce qu'il veut faire :**
- Trouver rapidement une voiture disponible pour une date et un lieu donnés.
- Voir le prix total avant de confirmer.
- Accéder à ses réservations passées pour retrouver un numéro de contrat.
- Contacter le support rapidement si un problème survient.

**Ce qui le frustre aujourd'hui :**
- Il doit créer un compte différent pour chaque pays.
- L'interface n'est pas adaptée au mobile.
- Le support ne répond que par e-mail, avec des délais de 24 à 48 heures.

**Besoins en accessibilité** : Aucun handicap identifié. Navigation standard.

---

### 4.2 Persona 2 — Le client en situation de handicap (PSH)

**Prénom fictif** : Sophie, 52 ans, consultante indépendante, malvoyante (utilise un lecteur d'écran NVDA)

**Situation** : Sophie a une déficience visuelle sévère. Elle navigue sur le web exclusivement au clavier et utilise un logiciel de lecture d'écran qui lit à voix haute le contenu des pages web.

**Ce qu'elle veut faire :**
- Accomplir exactement les mêmes tâches que n'importe quel autre client.
- Ne pas être bloquée par des éléments graphiques non décrits.
- Remplir des formulaires avec des indications claires sur ce qui est attendu.
- Être informée en temps réel des nouveaux messages dans le tchat.

**Ce qui la bloque aujourd'hui :**
- Les images de véhicules n'ont pas de texte alternatif : le lecteur d'écran dit "image" sans décrire la voiture.
- Les boutons sans label textuel sont illisibles pour le lecteur d'écran.
- Les messages d'erreur des formulaires ne sont pas annoncés automatiquement.
- Le tchat n'annonce pas les nouveaux messages à voix haute.

**Exigences spécifiques pour ce persona :**
- Tous les éléments interactifs sont accessibles au clavier (Tab, Entrée, Espace, flèches).
- Les images ont un attribut `alt` descriptif (ex : `alt="Renault Clio 2024, 5 places, boîte manuelle"`).
- Les messages d'erreur utilisent `aria-live` pour être annoncés automatiquement.
- Le tchat utilise `aria-live="polite"` pour annoncer les nouveaux messages.
- Le focus clavier est toujours visible (pas de `outline: none` dans le CSS).
- Le contraste texte/fond est ≥ 4,5:1 pour le texte normal (WCAG 1.4.3).

---

### 4.3 Persona 3 — Le client avec handicap moteur

**Prénom fictif** : Julien, 29 ans, développeur web, handicap moteur des mains (utilise un switch de navigation)

**Situation** : Julien ne peut pas utiliser une souris. Il navigue avec un switch (bouton unique) qui simule la touche Tab du clavier. Chaque pression avance d'un élément interactif.

**Exigences spécifiques :**
- L'ordre de navigation au clavier doit être logique (de haut en bas, de gauche à droite).
- Les formulaires longs doivent être découpés en étapes pour réduire la fatigue.
- Les sessions ne doivent pas expirer trop vite (30 minutes d'inactivité avec avertissement).
- Aucun contenu ne doit nécessiter un survol de souris (hover) pour être accessible.

---

### 4.4 Persona 4 — L'agent support client

**Prénom fictif** : Amina, 31 ans, conseillère clientèle au centre de support Paris

**Situation** : Amina passe ses journées à répondre aux clients par téléphone et par e-mail. Elle travaille sur un ordinateur de bureau avec deux écrans. Elle gère en moyenne 40 à 60 demandes par jour.

**Ce qu'elle veut faire :**
- Accéder immédiatement à la fiche d'un client à partir de son nom ou numéro de réservation.
- Gérer plusieurs conversations de tchat en même temps (au moins 3 simultanément).
- Modifier une réservation directement dans l'interface sans devoir appeler un autre service.
- Utiliser des réponses pré-rédigées pour les questions fréquentes (FAQ rapide).

**Ce qui la frustre aujourd'hui :**
- Elle doit jongler entre plusieurs outils non connectés (CRM, application web, e-mail).
- Elle ne peut pas voir les réservations d'un client en temps réel pendant qu'il lui parle.
- Il n'existe pas de tchat : tout passe par e-mail, ce qui est lent.

---

### 4.5 Persona 5 — L'administrateur système

**Prénom fictif** : Thomas, 45 ans, responsable informatique siège social

**Situation** : Thomas est le gardien des données de référence. Il gère les catalogues de véhicules, les agences, les tarifs et les droits d'accès des utilisateurs internes.

**Ce qu'il veut faire :**
- Ajouter un nouveau modèle de véhicule avec ses caractéristiques et photos.
- Désactiver temporairement une agence sans perdre son historique.
- Créer ou supprimer des comptes pour les agents support.
- Consulter les logs d'activité pour enquêter sur un incident.

**Ce qui le frustre aujourd'hui :**
- Il doit faire les modifications dans deux systèmes différents (Europe + Amérique du Nord).
- Il n'existe pas de log centralisé des actions sensibles.

---

## 5. Considérations transverses

Les considérations transverses s'appliquent à **toutes les fonctionnalités** du système, pas à une seule en particulier. Elles doivent être intégrées dès la conception, pas rajoutées à la fin.

### 5.1 Accessibilité

#### Pourquoi c'est une priorité légale et éthique

En France, la **loi du 11 février 2005** pour l'égalité des droits des personnes handicapées, renforcée par la **directive européenne 2016/2102**, impose aux entreprises de rendre leurs services numériques accessibles. Le non-respect expose l'entreprise à des sanctions et à des procédures judiciaires.

Au-delà de la loi, c'est une question d'éthique : 15 % de la population mondiale vit avec un handicap (OMS). Exclure ces utilisateurs représente aussi un manque à gagner commercial.

#### Les normes applicables

- **WCAG 2.1 niveau AA** (Web Content Accessibility Guidelines) : norme internationale, obligatoire pour tous les marchés.
- **RGAA 4.1** (Référentiel Général d'Amélioration de l'Accessibilité) : déclinaison française du WCAG, obligatoire pour les organismes publics et recommandée pour les entreprises privées en France.

#### Les 4 principes POUR (WCAG)

| Principe | Signification | Exemple concret |
|---|---|---|
| **Perceptible** | L'information doit être présentée de façon à ce que tous les utilisateurs puissent la percevoir | Image avec attribut `alt` pour les malvoyants |
| **Utilisable** | Les composants doivent être utilisables par tous | Navigation complète au clavier |
| **Compréhensible** | L'information et l'interface doivent être compréhensibles | Messages d'erreur clairs, en français |
| **Robuste** | Le contenu doit être interprétable par les technologies d'assistance | HTML sémantique, ARIA correct |

#### Exigences concrètes pour ce projet

- Tout bouton a un label textuel lisible par un lecteur d'écran.
- Toute image non décorative a un `alt` descriptif.
- Toute image décorative a `alt=""` pour être ignorée par le lecteur d'écran.
- Les formulaires ont des `<label>` associés à chaque champ.
- Les messages d'erreur sont annoncés via `aria-live`.
- Le tchat utilise `role="log"` et `aria-live="polite"`.
- Le ratio de contraste texte/fond est ≥ 4,5:1 (texte normal) et ≥ 3:1 (grand texte).
- Aucune fonctionnalité ne nécessite exclusivement la souris.

---

### 5.2 Sécurité et protection des données (RGPD)

#### Qu'est-ce que le RGPD ?

Le **Règlement Général sur la Protection des Données** (RGPD, entré en vigueur en mai 2018) est une loi européenne qui encadre la collecte, le stockage et l'utilisation des données personnelles. Son non-respect peut entraîner des amendes allant jusqu'à **4 % du chiffre d'affaires mondial** ou 20 millions d'euros.

#### Les droits des utilisateurs garantis par le RGPD

| Droit | Ce que ça signifie concrètement | Comment l'application y répond |
|---|---|---|
| **Droit d'accès** | L'utilisateur peut demander toutes ses données | Export JSON disponible dans le profil |
| **Droit de rectification** | L'utilisateur peut corriger ses données | Modification du profil à tout moment |
| **Droit à l'effacement** | L'utilisateur peut demander la suppression de son compte | Anonymisation sous 30 jours (voir ci-dessous) |
| **Droit à la portabilité** | L'utilisateur peut récupérer ses données dans un format standard | Export JSON ou CSV |
| **Droit d'opposition** | L'utilisateur peut s'opposer à certains traitements | Préférences de communication dans le profil |

#### Pourquoi "anonymisation" et pas "suppression" ?

Quand un client supprime son compte, ses messages dans le tchat ne peuvent pas être simplement supprimés : l'agent support a besoin de retrouver l'historique d'une conversation pour traiter un litige. La solution retenue est l'**anonymisation** : le contenu des messages est conservé, mais le nom de l'auteur est remplacé par "Utilisateur supprimé". Techniquement, le champ `author` de la table `Message` est mis à `NULL`.

#### Autres exigences de sécurité

- Les mots de passe sont stockés **hachés** (bcrypt ou Argon2), jamais en clair.
- Toutes les communications sont chiffrées en **HTTPS** (web) et **WSS** (tchat).
- Les formulaires sont protégés contre les attaques **CSRF** (Cross-Site Request Forgery).
- Les sessions expirent après 30 minutes d'inactivité.
- Les tentatives de connexion sont limitées (blocage temporaire après 5 échecs).
- Les actions sensibles sont tracées dans un **log d'audit** (qui a fait quoi, quand).

---

### 5.3 Internationalisation (i18n)

#### Qu'est-ce que l'internationalisation ?

L'internationalisation (abrégée "i18n" car il y a 18 lettres entre le "i" et le "n") est la capacité d'une application à s'adapter à différentes langues et cultures **sans modifier son code**.

#### Ce que ça implique concrètement

- Tous les textes de l'interface sont stockés dans des **fichiers de traduction** (format `.po`/`.mo`), pas directement dans le code.
- La langue est détectée automatiquement depuis les préférences du navigateur, et peut être changée manuellement dans le profil.
- Les **dates** s'affichent selon les conventions locales : `25/04/2026` en France, `04/25/2026` aux États-Unis.
- Les **monnaies** sont adaptées : EUR (€) en Europe, USD ($) et CAD (CA$) en Amérique du Nord.
- Les **nombres** suivent les conventions locales : `1 234,56` en France vs `1,234.56` aux États-Unis.

**Langues supportées au lancement** : Français (FR), Anglais (EN), Espagnol (ES)  
**Architecture extensible** : ajouter une nouvelle langue ne nécessite que de traduire les fichiers `.po`, sans toucher au code.

---

## 6. Spécifications fonctionnelles — User Stories

### Comment lire une user story ?

Une **user story** (histoire utilisateur) décrit une fonctionnalité du point de vue de l'utilisateur, selon ce format :

> **En tant que** [type d'utilisateur],  
> **je veux** [action que je veux réaliser],  
> **afin de** [bénéfice que j'en tire].

Les **critères d'acceptation** (CA) sont les conditions précises qui doivent être remplies pour que la fonctionnalité soit considérée comme "terminée". Ils servent de base aux tests.

---

### Module 1 — Gestion des comptes et authentification

Ce module est le **prérequis** de toutes les autres fonctionnalités : sans compte, pas de réservation, pas de tchat.

---

#### US-01 — Créer un compte client

> **En tant que** visiteur non connecté,  
> **je veux** créer un compte personnel,  
> **afin de** pouvoir réserver des véhicules et bénéficier d'un suivi personnalisé.

**Pourquoi c'est important** : Aujourd'hui, un client doit créer un compte par pays. Un compte unique centralisé est la pierre angulaire de toute l'unification.

**Critères d'acceptation :**

| # | Critère | Détail |
|---|---|---|
| CA-01-1 | Champs obligatoires | Prénom, nom, e-mail, mot de passe, pays de résidence, langue préférée |
| CA-01-2 | Validation e-mail | Un e-mail de confirmation est envoyé. Le compte reste inactif jusqu'à validation du lien (valable 24h) |
| CA-01-3 | Règles mot de passe | Minimum 8 caractères, dont au moins 1 majuscule, 1 minuscule et 1 chiffre |
| CA-01-4 | E-mail déjà utilisé | Message d'erreur clair : "Cette adresse e-mail est déjà associée à un compte. Connectez-vous ou réinitialisez votre mot de passe." |
| CA-01-5 | Accessibilité | Formulaire navigable au clavier, chaque champ a un `<label>`, les erreurs sont annoncées par le lecteur d'écran |
| CA-01-6 | RGPD | Une case à cocher explicite (non pré-cochée) valide l'acceptation de la politique de confidentialité |

---

#### US-02 — Se connecter à son compte

> **En tant que** client inscrit,  
> **je veux** me connecter avec mon e-mail et mon mot de passe,  
> **afin d'** accéder à mon espace personnel et mes réservations.

**Critères d'acceptation :**

| # | Critère | Détail |
|---|---|---|
| CA-02-1 | Connexion réussie | Redirection vers le tableau de bord personnel après connexion |
| CA-02-2 | Erreur de connexion | Message générique "E-mail ou mot de passe incorrect" (pas de précision sur lequel est faux, pour des raisons de sécurité) |
| CA-02-3 | Protection brute force | Blocage temporaire de 15 minutes après 5 tentatives échouées consécutives |
| CA-02-4 | Mot de passe oublié | Lien "Mot de passe oublié" sur la page de connexion, envoi d'un lien de réinitialisation valable 1 heure |
| CA-02-5 | Expiration de session | La session expire après 30 minutes d'inactivité avec un avertissement 5 minutes avant |
| CA-02-6 | Accessibilité | Formulaire entièrement navigable au clavier, messages d'erreur accessibles |

---

#### US-03 — Gérer son profil

> **En tant que** client connecté,  
> **je veux** consulter et modifier mes informations personnelles,  
> **afin de** maintenir mes données à jour et personnaliser mon expérience.

**Critères d'acceptation :**

| # | Critère | Détail |
|---|---|---|
| CA-03-1 | Informations modifiables | Prénom, nom, téléphone, adresse postale, langue d'interface, pays |
| CA-03-2 | Changement d'e-mail | Nécessite une confirmation par lien envoyé à la nouvelle adresse |
| CA-03-3 | Changement de mot de passe | Saisie du mot de passe actuel requis pour valider |
| CA-03-4 | Export RGPD | Bouton "Télécharger mes données" → fichier JSON contenant toutes les données du compte |
| CA-03-5 | Suppression de compte | Bouton "Supprimer mon compte" avec étape de confirmation + délai d'anonymisation de 30 jours |
| CA-03-6 | Confirmation des modifications | Un message de succès s'affiche après chaque modification enregistrée |

---

### Module 2 — Recherche et réservation de véhicules

Ce module est le **cœur de métier** de Your Car Your Way. C'est la fonctionnalité la plus utilisée et celle qui génère le chiffre d'affaires.

---

#### US-04 — Rechercher un véhicule disponible

> **En tant que** visiteur ou client connecté,  
> **je veux** rechercher un véhicule disponible en fonction de mes critères,  
> **afin de** trouver rapidement une offre adaptée à mes besoins.

**Critères d'acceptation :**

| # | Critère | Détail |
|---|---|---|
| CA-04-1 | Critères de recherche | Lieu de prise en charge (ville ou agence), lieu de restitution (optionnel, sinon identique), date/heure de départ, date/heure de retour |
| CA-04-2 | Filtres | Catégorie (citadine, berline, SUV, utilitaire), nombre de places minimum, type de transmission (manuelle/automatique), type de carburant |
| CA-04-3 | Résultats affichés | Photo, marque/modèle, catégorie, nombre de places, transmission, carburant, prix par jour, disponibilité |
| CA-04-4 | Tri des résultats | Par prix croissant, prix décroissant, pertinence |
| CA-04-5 | Accessibilité images | Chaque photo a un `alt` descriptif : "Renault Clio 2024, citadine, 5 places, boîte manuelle, 45€/jour" |
| CA-04-6 | Résultats vides | Message clair et suggestion d'élargir les critères si aucun véhicule n'est disponible |
| CA-04-7 | Performance | Les résultats s'affichent en moins de 2 secondes |

---

#### US-05 — Réserver un véhicule

> **En tant que** client connecté,  
> **je veux** réserver un véhicule sélectionné pour des dates précises,  
> **afin de** garantir sa disponibilité lors de mon déplacement.

**Critères d'acceptation :**

| # | Critère | Détail |
|---|---|---|
| CA-05-1 | Récapitulatif avant confirmation | Véhicule, agences de départ/retour, dates, durée, options sélectionnées, prix total TTC |
| CA-05-2 | Confirmation explicite | Bouton "Confirmer la réservation" clairement identifié, sans ambiguïté |
| CA-05-3 | E-mail de confirmation | Envoi immédiat avec numéro de réservation, détails complets, coordonnées de l'agence |
| CA-05-4 | Véhicule plus disponible | Si le véhicule est réservé par un autre client entre la sélection et la confirmation, message d'erreur clair et redirection vers des alternatives |
| CA-05-5 | Accessibilité | Processus de réservation entièrement navigable au clavier, étapes clairement annoncées |
| CA-05-6 | Connexion requise | Si le visiteur n'est pas connecté, redirection vers la connexion, puis retour au processus de réservation |

---

#### US-06 — Consulter et gérer ses réservations

> **En tant que** client connecté,  
> **je veux** voir la liste de toutes mes réservations passées et à venir,  
> **afin de** les gérer et préparer mes déplacements.

**Critères d'acceptation :**

| # | Critère | Détail |
|---|---|---|
| CA-06-1 | Statuts affichés | À venir, En cours, Terminée, Annulée — chacun avec une couleur distincte |
| CA-06-2 | Annulation | Possible si la date de prise en charge est à plus de 48 heures. Sinon, message d'information avec contact support |
| CA-06-3 | Téléchargement contrat | Bouton "Télécharger le contrat PDF" disponible pour chaque réservation confirmée |
| CA-06-4 | Historique | Remonte sur les 24 derniers mois minimum |
| CA-06-5 | Détail réservation | Clic sur une réservation ouvre le détail complet (véhicule, agences, dates, prix, statut) |

---

### Module 3 — Tchat client / support en temps réel

Le tchat est la **fonctionnalité différenciatrice** de ce projet. Elle remplace le support uniquement par e-mail qui génère des délais de réponse insatisfaisants.

> **Qu'est-ce que le "temps réel" ?** Aujourd'hui, si un client envoie un e-mail au support, il attend en général 24 à 48 heures une réponse. Avec le tchat en temps réel, le message apparaît instantanément chez l'agent, et la réponse apparaît instantanément chez le client — comme une messagerie instantanée (WhatsApp, Teams).

---

#### US-07 — Démarrer une conversation de tchat

> **En tant que** client connecté,  
> **je veux** ouvrir une conversation de tchat avec le support,  
> **afin d'** obtenir une réponse rapide à ma question sans attendre au téléphone ou par e-mail.

**Critères d'acceptation :**

| # | Critère | Détail |
|---|---|---|
| CA-07-1 | Accessibilité du bouton | Bouton "Contacter le support" visible sur toutes les pages, y compris la fiche d'une réservation |
| CA-07-2 | Temps de connexion | La connexion au tchat s'établit en moins de 3 secondes |
| CA-07-3 | Historique de session | Le client retrouve les messages de sa conversation en cours dès sa reconnexion |
| CA-07-4 | Message de bienvenue | Message automatique indiquant le délai de réponse estimé et les horaires du support |
| CA-07-5 | Accessibilité | Zone de tchat avec `role="log"` et `aria-live="polite"` pour annoncer les nouveaux messages aux lecteurs d'écran |

---

#### US-08 — Envoyer et recevoir des messages en temps réel

> **En tant que** client ou agent support,  
> **je veux** envoyer des messages qui apparaissent instantanément chez mon interlocuteur,  
> **afin de** mener une conversation fluide et efficace.

**Critères d'acceptation :**

| # | Critère | Détail |
|---|---|---|
| CA-08-1 | Instantanéité | Le message apparaît chez le destinataire en moins de 500 millisecondes après envoi |
| CA-08-2 | Horodatage | Chaque message affiche l'heure d'envoi (format HH:MM) |
| CA-08-3 | Indicateur de lecture | Un indicateur visuel ("Lu") s'affiche quand le message a été vu par le destinataire |
| CA-08-4 | Limite de caractères | Un message est limité à 2 000 caractères avec compteur affiché |
| CA-08-5 | Reconnexion automatique | Si la connexion est perdue, un message d'avertissement s'affiche et une tentative de reconnexion est lancée automatiquement toutes les 5 secondes |
| CA-08-6 | Protection XSS | Les messages sont échappés avant affichage pour empêcher l'injection de code malveillant |

---

#### US-09 — Gérer plusieurs conversations simultanées (agent)

> **En tant qu'** agent support,  
> **je veux** gérer plusieurs conversations en même temps depuis un tableau de bord unifié,  
> **afin de** traiter les demandes efficacement sans perdre le fil d'aucune conversation.

**Critères d'acceptation :**

| # | Critère | Détail |
|---|---|---|
| CA-09-1 | Liste des conversations | Colonne latérale listant toutes les conversations actives |
| CA-09-2 | Distinction visuelle | Les conversations avec des messages non lus sont mises en évidence (badge, couleur) |
| CA-09-3 | Transfert | L'agent peut transférer une conversation à un collègue avec une note de contexte |
| CA-09-4 | Clôture | L'agent peut marquer une conversation comme "Résolue" ce qui la déplace dans les archives |
| CA-09-5 | Accès fiche client | En ouvrant une conversation, l'agent voit directement la fiche du client et ses réservations en cours |

---

### Module 4 — Administration et back-office

Ce module est réservé aux **administrateurs internes** de Your Car Your Way. Il n'est pas visible par les clients.

---

#### US-10 — Gérer le catalogue de véhicules

> **En tant qu'** administrateur,  
> **je veux** ajouter, modifier et désactiver des véhicules dans le catalogue,  
> **afin que** l'offre présentée aux clients soit toujours à jour.

**Critères d'acceptation :**

| # | Critère | Détail |
|---|---|---|
| CA-10-1 | Champs d'un véhicule | Marque, modèle, année, catégorie, nombre de places, transmission, carburant, photo principale, description, prix de base par jour, agence de rattachement |
| CA-10-2 | Protection des données liées | La suppression définitive d'un véhicule ayant des réservations futures est bloquée avec un message explicatif. Seule la désactivation est possible |
| CA-10-3 | Traçabilité | Chaque modification (qui a modifié quoi, quand) est enregistrée dans le log d'audit |
| CA-10-4 | Upload photo | L'administrateur peut téléverser une photo (formats JPG, PNG, max 5 Mo) |

---

#### US-11 — Gérer les agences

> **En tant qu'** administrateur,  
> **je veux** gérer la liste des agences et leurs informations,  
> **afin que** les clients trouvent facilement les informations d'une agence.

**Critères d'acceptation :**

| # | Critère | Détail |
|---|---|---|
| CA-11-1 | Champs d'une agence | Nom, adresse complète, ville, pays, coordonnées GPS (latitude/longitude), téléphone, e-mail, horaires d'ouverture |
| CA-11-2 | Désactivation temporaire | Une agence peut être désactivée (fermeture travaux, etc.) sans être supprimée, ce qui masque ses véhicules aux clients |
| CA-11-3 | Affichage carte | Les coordonnées GPS permettent d'afficher l'agence sur une carte interactive |

---

#### US-12 — Gérer les utilisateurs et les droits d'accès

> **En tant qu'** administrateur,  
> **je veux** gérer les comptes des agents support et des autres administrateurs,  
> **afin de** contrôler qui a accès à quoi dans l'application.

**Critères d'acceptation :**

| # | Critère | Détail |
|---|---|---|
| CA-12-1 | Rôles disponibles | Client, Agent support, Administrateur |
| CA-12-2 | Création de compte agent | L'administrateur peut créer un compte agent directement (sans e-mail de confirmation) |
| CA-12-3 | Désactivation | Un compte peut être désactivé sans être supprimé (données conservées pour l'audit) |
| CA-12-4 | Log d'accès | Les connexions des agents et administrateurs sont enregistrées |

---

## 7. Priorisation MoSCoW

La méthode **MoSCoW** classe les fonctionnalités en 4 niveaux de priorité :
- **Must have** : indispensable, sans ça l'application ne peut pas être livrée.
- **Should have** : important, mais une solution de contournement temporaire est possible.
- **Could have** : utile si le temps et le budget le permettent.
- **Won't have** (pour cette version) : hors périmètre pour l'instant.

| Fonctionnalité | Priorité | Justification |
|---|---|---|
| Compte unique + authentification | **Must** | Prérequis de tout le reste |
| Recherche et réservation de véhicules | **Must** | Cœur de métier, génère le CA |
| Accessibilité WCAG 2.1 AA | **Must** | Obligation légale (RGAA) |
| Conformité RGPD | **Must** | Obligation légale (amende CNIL) |
| Tchat temps réel | **Should** | Fort différenciateur, mais e-mail reste utilisable temporairement |
| Historique réservations (24 mois) | **Should** | Satisfaction client élevée |
| Export PDF des contrats | **Should** | Service attendu mais non bloquant au lancement |
| Back-office administrateur | **Should** | Opérationnel mais visible uniquement en interne |
| Export RGPD (téléchargement données) | **Could** | Obligatoire légalement mais rarement utilisé |
| Internationalisation ES | **Could** | Marché hispanophone secondaire au lancement |
| Gestion des tarifs dynamiques | **Won't** | Trop complexe pour cette version |
| Paiement en ligne | **Won't** | Phase 2 avec prestataire dédié |

---

## 8. Contraintes et hypothèses

### 8.1 Contraintes

| Type | Contrainte | Impact |
|---|---|---|
| **Légale** | RGPD obligatoire | Conception des données et formulaires doit intégrer les droits des utilisateurs |
| **Légale** | WCAG 2.1 AA obligatoire | Chaque composant UI doit être testé pour l'accessibilité |
| **Technique** | Migration progressive | L'ancienne application Europe reste opérationnelle pendant la transition |
| **Technique** | Données existantes à migrer | Un plan de migration de données (hors périmètre PoC) est à prévoir |
| **Organisationnelle** | Équipe de taille moyenne | Architecture non surdimensionnée (pas de microservices) |

### 8.2 Hypothèses

Les hypothèses sont des éléments supposés vrais mais non encore confirmés. Si elles s'avèrent fausses, le périmètre ou les délais devront être renegociés.

- La direction validera les priorisations MoSCoW avant le début du développement.
- Les équipes terrain (agents support) seront disponibles pour des sessions de test utilisateur.
- Un serveur Redis sera disponible dans l'infrastructure cloud choisie.
- Le prestataire de paiement sera défini en phase 2 (exclu de ce périmètre).

---

## 9. Glossaire

| Terme | Définition simple |
|---|---|
| **ASGI** | Interface de programmation qui permet à un serveur web de gérer des connexions persistantes (comme le tchat). Remplace WSGI qui ne le supporte pas. |
| **ARIA** | Ensemble d'attributs HTML spéciaux qui aident les lecteurs d'écran à comprendre une page web. Ex : `aria-live`, `role="button"`. |
| **Brute force** | Technique d'attaque qui consiste à essayer des milliers de mots de passe jusqu'à trouver le bon. |
| **CSRF** | Cross-Site Request Forgery — type d'attaque où un site malveillant envoie des actions à votre place sur un autre site. Les tokens CSRF l'empêchent. |
| **i18n** | Abréviation d'internationalisation (18 lettres entre i et n). Capacité d'un logiciel à s'adapter à plusieurs langues sans changer son code. |
| **ORM** | Object-Relational Mapping — outil qui permet d'interagir avec une base de données en écrivant du code Python plutôt que du SQL. |
| **Persona** | Profil fictif représentant un type d'utilisateur, utilisé pour concevoir l'application en se mettant à la place de chaque utilisateur. |
| **PoC** | Proof of Concept — démonstration technique limitée prouvant qu'une fonctionnalité est réalisable avec la technologie choisie. |
| **PSH** | Personne en Situation de Handicap — terme générique incluant tous types de handicaps (visuel, moteur, cognitif, auditif). |
| **RGAA** | Référentiel Général d'Amélioration de l'Accessibilité — norme française d'accessibilité web, déclinaison du WCAG. |
| **RGPD** | Règlement Général sur la Protection des Données — loi européenne sur la vie privée, en vigueur depuis mai 2018. |
| **Room** | Salon de tchat virtuel. Dans ce projet, chaque conversation client/support correspond à une room. |
| **User story** | Façon de décrire une fonctionnalité du point de vue de l'utilisateur, en expliquant qui fait quoi et pourquoi. |
| **WCAG** | Web Content Accessibility Guidelines — norme internationale pour l'accessibilité du web, éditée par le W3C. |
| **WebSocket** | Protocole de communication qui maintient une connexion permanente entre le navigateur et le serveur, permettant l'échange de messages en temps réel. |
| **XSS** | Cross-Site Scripting — type d'attaque où du code malveillant est injecté dans une page web. L'échappement du HTML l'empêche. |
