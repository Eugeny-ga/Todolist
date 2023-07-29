from django.contrib import admin

from bot.models import TgUser


@admin.register(TgUser)
class TgUserAdmin(admin.ModelAdmin):
    list_display = ("chat_id", 'username')
    readonly_fields = ['verification_code']
    search_fields = ['chat_id', 'username']

# связывание модели на 23 мин