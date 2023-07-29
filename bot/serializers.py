from rest_framework import serializers

from bot.models import TgUser


class VerifySerializer(serializers.Serializer):
    verification_code = serializers.CharField(max_length=16)


class TgUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TgUser
        fields = "__all__"
