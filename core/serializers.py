from django.contrib.auth.hashers import make_password
from rest_framework import serializers, request
from rest_framework.exceptions import ValidationError, NotAuthenticated
from django.utils.translation import gettext_lazy as _
from core.models import User
from todolist.fields import PasswordField


class UserCreateSerializer(serializers.ModelSerializer):
    # Кастомное поле с настройкой валидаторов паролей и стиля ввода в форме паролей.
    password_repeat = PasswordField()
    password = PasswordField(validate=False)

    def validate(self, attrs):
        if attrs.get('password') == attrs.get('password_repeat'):
            return attrs
        raise ValidationError(_('Passwords are different'))

    def create(self, validated_data):
        del validated_data['password_repeat']
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name',
                  'email', 'password', 'password_repeat']


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = PasswordField(validate=False) #С отменой валидаторов

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']



class UpdatePasswordSerializer(serializers.Serializer):
    old_password = PasswordField(validate=False)
    new_password = PasswordField()

    def validate_old_password(self, old_password):
        request = self.context['request']

        if not request.user.is_authenticated:
            raise NotAuthenticated

        #Проверка старого пароля на совпадение с базой
        if not request.user.check_password(old_password):
            raise ValidationError(_('Password is incorrect'))

        return old_password
