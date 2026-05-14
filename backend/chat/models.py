from django.db import models
from django.contrib.auth.models import User


class Room(models.Model):
    """
    Représente une session de tchat entre un client et un agent.
    Dans le contexte Your Car Your Way, chaque réservation peut
    ouvrir une room dédiée.
    """

    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    participants = models.ManyToManyField(
        User,
        related_name="rooms",
        blank=True,
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Salon de tchat"
        verbose_name_plural = "Salons de tchat"

    def __str__(self):
        return self.name


class Message(models.Model):
    """
    Un message envoyé dans un salon de tchat.
    La relation vers User est nullable pour pouvoir conserver
    les messages après suppression d'un compte (RGPD : anonymisation).
    """

    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="messages")
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="messages",
    )
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["sent_at"]
        verbose_name = "Message"
        verbose_name_plural = "Messages"

    def __str__(self):
        author_name = self.author.username if self.author else "Utilisateur supprimé"
        return f"[{self.room.name}] {author_name} : {self.content[:50]}"
