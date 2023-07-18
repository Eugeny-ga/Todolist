from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.db import models
FullCheckPasswordValidator = []

class User(AbstractUser):
    MALE = "m"
    FEMALE = "f"
    SEX = [(MALE, _("Male")), (FEMALE, _("Female"))]
    sex = models.CharField(_("sex"), max_length=1, choices=SEX)
    birth_day = models.DateField(_("birth_day"), null=True, blank=True)



    def __str__(self):
        return self.username
