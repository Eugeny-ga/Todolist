
from rest_framework import serializers


class PasswordRepeatValidator:
    def __init__(self, password):
        self.password = password

    def __call__(self, password_repeat):
        if self.password != password_repeat:
            raise serializers.ValidationError("Incorrect repeat password")