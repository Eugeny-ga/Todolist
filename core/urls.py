from django.urls import path

from core.views import UserCreateAPIView, LoginView, ProfileView, UpdatePasswordView

urlpatterns = [
    path('signup', UserCreateAPIView.as_view(), name='signup'),  # Создание пользователя
    path('login', LoginView.as_view(), name='login'),  # Авторизация
    path('profile', ProfileView.as_view(), name='profile'),  # Редактирование профиля пользователя
    path('update_password', UpdatePasswordView.as_view(), name='update_password'),
]