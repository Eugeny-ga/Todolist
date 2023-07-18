from django.urls import path

from core.views import UserCreateAPIView, LoginView, ProfileView, UpdatePasswordView

urlpatterns = [
    path('signup', UserCreateAPIView.as_view(), name='signup'),
    path('login', LoginView.as_view(), name='login'),
    path('profile', ProfileView.as_view(), name='profile'),
    path('update_password', UpdatePasswordView.as_view(), name='update_password'),
]