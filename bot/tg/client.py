import logging
from typing import TypeVar, Type
import requests
from pydantic import ValidationError
from pydantic.main import BaseModel
from bot.tg.classes import GetUpdatesResponse, SendMessageResponse


T = TypeVar('T', bound=BaseModel)

logger = logging.getLogger(__name__)

class TgClient:
    def __init__(self, token):
        self._token = token

    def _get_url(self, method: str):
        return f"https://api.telegram.org/bot{self._token}/{method}"

    def get_updates(self, offset: int = 0, timeout: int = 10) -> GetUpdatesResponse:
        method = 'getUpdates'
        url = self._get_url(method)

        params = {'timeout': timeout, 'offset': offset, 'allowed_updates': ['message']}
        response = requests.get(url, params=params)

        if response.ok:
            data = response.json()
            return self._deserialize_tg_response(GetUpdatesResponse, data)
        else:
            logger.error('Bad request getUpdates')

    def send_message(self, chat_id: int, text: str, timeout: int = 10) -> SendMessageResponse:
        method = 'sendMessage'
        url = self._get_url(method)

        params = {'timeout': timeout, 'chat_id': chat_id, 'text': text}
        response = requests.get(url, params=params)

        if response.ok:
            data = response.json()
            return self._deserialize_tg_response(SendMessageResponse, data)
        else:
            logger.warning('Bad request sendMessage')

    @staticmethod
    def _deserialize_tg_response(serializer_class: Type[T], data: dict) -> T:
        try:
            return serializer_class(**data)
        except ValidationError:
            logger.error(f'Failed to deserialize JSON response: {data}')







