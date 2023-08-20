from django.core.management import BaseCommand, CommandError

from bot.models import TgUser
from bot.tg.classes import Message
from bot.tg.client import TgClient
from bot.tg.service import get_categories_from_db, get_goals_from_db
from todolist.settings import TG_TOKEN


class Command(BaseCommand):
    help = "Запуск телеграм-бота"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tg_client = TgClient(TG_TOKEN)
        self.users_data = {}

    def handle(self, *args, **options) -> None:
        offset = 0
        try:
            while True:
                response = self.tg_client.get_updates(offset=offset)

                for item in response.result:
                    offset = item.update_id + 1
                    self.handle_message(item.message)
        except Exception as e:
            raise CommandError(f'Произошла ошибка: {e}')

    def handle_message(self, message: Message) -> None:
        # get the chat id with user from response
        chat_id = message.chat.id
        # get a telegram user from the database or create it.
        tg_user, _ = TgUser.objects.get_or_create(chat_id=chat_id)

        # if tg-user is not associated with users, authorize it
        if not tg_user.is_verified:
            tg_user.update_verification_code()
            message = f"Вы новый пользователь. Ваш код верификации - {tg_user.verification_code}"
            self.tg_client.send_message(chat_id=chat_id, text=message)
        else:
            self.handle_auth_user(tg_user=tg_user, message=message)

    def handle_auth_user(self, tg_user: TgUser, message: Message) -> None:
        # Processing commands from the user
        if message.text.startswith('/'):
            match message.text:
                case '/goals':
                    text = get_goals_from_db(tg_user.user.id)
                case '/create':
                    text = get_categories_from_db(user_id=tg_user.user.id, chat_id=message.chat.id, users_data=self.users_data)
                case '/cancel':
                    if self.users_data[message.chat.id]:
                        del self.users_data[message.chat.id]
                    text = 'Выход'
                case _:
                    text = 'Неизвестная команда'

        # Processing user responses. Handlers: choose_category, create_goal
        elif self.users_data.get(message.chat.id):
            next_handler = self.users_data[message.chat.id].get('next_handler')
            text = next_handler(
                user_id=tg_user.user.id, chat_id=message.chat.id, message=message.text, users_data=self.users_data
            )

        # Re-output commands to user if the request is not correct
        else:
            text = (
                'Список команд:\n'
                '/goals - Список целей\n'
                '/create - Создать цель\n'
                '/cancel - Выйти'
            )

        self.tg_client.send_message(chat_id=message.chat.id, text=text)

