"""
Modèles de données de l'application tchat.
Deux entités : Room (salon) et Message.
"""

from django.db import models
from django.contrib.auth.models import User


class Room(models.Model):
    """
    Représente un salon de tchat entre un client et un agent support.
    Chaque réservation peut ouvrir une room dédiée.
    """

    # Nom unique du salon — sert d'identifiant dans l'URL WebSocket
    name = models.CharField(max_length=100, unique=True)

    # Date de création automatique à la première sauvegarde
    created_at = models.DateTimeField(auto_now_add=True)

    # Liste des utilisateurs autorisés à accéder à ce salon
    # Many-to-Many : un user peut avoir plusieurs rooms, une room plusieurs users
    participants = models.ManyToManyField(
        User,
        related_name="rooms",  # permet d'écrire user.rooms.all()
        blank=True,            # le champ est optionnel (pas de participants au départ)
    )

    class Meta:
        # Tri par date décroissante : les rooms les plus récentes en premier
        ordering = ["-created_at"]
        verbose_name = "Salon de tchat"
        verbose_name_plural = "Salons de tchat"

    def __str__(self):
        # Représentation textuelle affichée dans l'admin Django
        return self.name


class Message(models.Model):
    """
    Un message envoyé dans un salon de tchat.

    Décision RGPD : le champ 'author' est nullable (null=True).
    Quand un utilisateur supprime son compte, ses messages sont conservés
    (l'historique reste utile pour le support) mais l'auteur est mis à NULL
    via SET_NULL — c'est de l'anonymisation, pas de la suppression.
    """

    # Room à laquelle appartient le message
    # CASCADE : si la room est supprimée, tous ses messages le sont aussi
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name="messages",  # permet d'écrire room.messages.all()
    )

    # Auteur du message — nullable pour la conformité RGPD
    # SET_NULL : si l'utilisateur supprime son compte, author devient NULL
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,   # autorise NULL en base de données
        blank=True,  # autorise le champ vide dans les formulaires Django
        related_name="messages",
    )

    # Contenu texte du message
    content = models.TextField()

    # Horodatage automatique à l'envoi — non modifiable
    sent_at = models.DateTimeField(auto_now_add=True)

    # Indicateur de lecture pour l'interface ("Lu" côté destinataire)
    is_read = models.BooleanField(default=False)

    class Meta:
        # Tri chronologique : du plus ancien au plus récent
        ordering = ["sent_at"]
        verbose_name = "Message"
        verbose_name_plural = "Messages"

    def __str__(self):
        # Affiche "nom_auteur" ou "Utilisateur supprimé" si author est NULL
        author_name = self.author.username if self.author else "Utilisateur supprimé"
        return f"[{self.room.name}] {author_name} : {self.content[:50]}"
