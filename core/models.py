from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    MALE = "m"
    FEMALE = "f"
    SEX = [(MALE, _("Male")), (FEMALE, _("Female"))]

    sex = models.CharField(max_length=1, choices=SEX)
    birth_day = models.DateField(null=True, blank=True)
