import strawberry
from strawberry import auto
from . import models


@strawberry.django.type(models.User)
class UserType:
    username: auto
    email: auto
    name: auto
