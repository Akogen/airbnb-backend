from django.db import models
from common.models import AbstractTimeStamp


class Experience(AbstractTimeStamp):
    """Experience Model Definition"""

    name = models.CharField(max_length=250)
    description = models.TextField()
    country = models.CharField(
        max_length=80,
        default="United State of America",
    )
    city = models.CharField(
        max_length=80,
        default="Los Angeles",
    )
    address = models.CharField(
        max_length=250,
        default="",
    )
    price = models.PositiveIntegerField()

    start = models.TimeField()
    end = models.TimeField()

    host = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="experiences",
    )
    perks = models.ManyToManyField(
        "Perk",
        related_name="experiences",
    )
    category = models.ForeignKey(
        "categories.Category",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="experiences",
    )

    def __str__(self) -> str:
        return self.name


class Perk(AbstractTimeStamp):
    """What is included on an Experience"""

    name = models.CharField(
        max_length=100,
    )
    details = models.CharField(
        max_length=250,
        blank=True,
        default="",
    )
    explanation = models.TextField(
        blank=True,
        default="",
    )

    def __str__(self) -> str:
        return self.name
