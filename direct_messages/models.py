from django.db import models
from common.models import AbstractTimeStamp


class ChattingRoom(AbstractTimeStamp):
    """Room Model Definition"""

    users = models.ManyToManyField(
        "users.User",
        related_name="chattingrooms",
    )

    def __str__(self):
        return "Chatting Room"


class Message(AbstractTimeStamp):
    """Message Model Definition"""

    text = models.TextField()
    user = models.ForeignKey(
        "users.User",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="messages",
    )
    room = models.ForeignKey(
        "direct_messages.ChattingRoom",
        on_delete=models.CASCADE,
        related_name="messages",
    )

    def __str__(self):
        return f"{self.user} says: {self.text}"
