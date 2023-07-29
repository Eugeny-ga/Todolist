from django.db import models
from django.utils.crypto import get_random_string

from core.models import User


class TgUser(models.Model):

    chat_id = models.PositiveBigIntegerField(primary_key=True, editable=False, unique=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    # если юзер связан, то авторизация пройдена.
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    # подтверждение пользователя
    verification_code = models.CharField(max_length=16, null=True, blank=True, unique=True)

    @property
    def is_verified(self):
        return bool(self.user)

    @staticmethod
    def _generate_verification_code():
        return get_random_string(16)

    def update_verification_code(self):
        self.verification_code = self._generate_verification_code()
        self.save(update_fields=['verification_code'])

    def __str__(self):
        return f'Telegram-user ({self.chat_id})'

    class Meta:
        verbose_name = 'Пользователь телеграм'
        verbose_name_plural = 'Пользователи телеграм'
