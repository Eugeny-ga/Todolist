from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers


class PasswordField(serializers.CharField):
    def __init__(self, validate: bool = True, *args, **kwargs):
        #Ставим значение словаря, если оно не установлено.
        kwargs.setdefault("write_only", True)
        kwargs.setdefault("required", True)

        #Скрываем пароль за звездочками в окне ввода пароля
        kwargs['style'] = {'input_type': 'password'}
        super().__init__(**kwargs)

        #Выполнение валидаторов пароля, если параметр validate = True
        if validate:
            self.validators.append(validate_password)
