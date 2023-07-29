from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from bot.models import TgUser
from bot.serializers import VerifySerializer, TgUserSerializer
from bot.tg.client import TgClient
from todolist.settings import TG_TOKEN


class VerificationView(APIView):
    serializer_class = VerifySerializer
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request):
        # Десериализация кода верификации
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            verification_code = serializer.validated_data.get('verification_code')

            tg_user = TgUser.objects.get(verification_code=verification_code)
            # Связываем тг-юзера и юзера
            if tg_user:
                tg_user.user_id = request.user.id
                tg_user.save()

                tg_user_serializer = TgUserSerializer(tg_user)
                client = TgClient(TG_TOKEN)
                client.send_message(chat_id=tg_user.chat_id, text='Верификация прошла успешно!')

                return Response(tg_user_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response('Пользователь не найден', status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

