from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.db import models
FullCheckPasswordValidator = []

class User(AbstractUser):

    def __str__(self):
        return self.username

