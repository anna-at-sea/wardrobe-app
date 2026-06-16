from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    class Meta:
        verbose_name = "User"

    email = models.EmailField(
        "email address", blank=False, unique=True,
        error_messages={
            "unique": "A user with that email already exists."
        },
    )

    def __str__(self):
        return self.username
