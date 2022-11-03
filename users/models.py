from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom User Model Definition"""

    class GenderChoices(models.TextChoices):
        MALE = ("male", "Male")
        FEMALE = ("female", "Female")

    class LanguageChoices(models.TextChoices):
        EN = ("en", "English")
        KR = ("kr", "Korean")

    class CurrencyChoices(models.TextChoices):
        USD = ("usd", "US, Dollar")
        KRW = ("krw", "South Korean, Won")

    first_name = models.CharField(
        max_length=150,
        editable=False,
    )
    last_name = models.CharField(
        max_length=150,
        editable=False,
    )
    # avatar = models.ImageField(upload_to="user_photos", blank=True)
    avatar = models.URLField(blank=True)
    name = models.CharField(
        max_length=150,
        default="",
    )
    gender = models.CharField(
        max_length=10,
        blank=True,
        choices=GenderChoices.choices,
        null=True,
    )
    bio = models.TextField(default="")
    birthdate = models.DateField(
        blank=True,
        null=True,
    )
    language = models.CharField(
        max_length=2,
        blank=True,
        choices=LanguageChoices.choices,
        null=True,
    )
    currency = models.CharField(
        max_length=3,
        blank=True,
        choices=CurrencyChoices.choices,
        null=True,
    )
    is_host = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.name} - {self.username}"
