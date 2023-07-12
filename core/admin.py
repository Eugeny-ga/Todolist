from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from core.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    readonly_fields = ('last_login', 'date_joined')
    exclude = ("password",)
    list_display = ("username", "first_name", "last_name", "email")
    list_filter = ("is_staff", "is_superuser", "is_active")
    search_fields = ("username", "first_name", "last_name")

