from pydantic import BaseModel


class Chat(BaseModel):
    id: int
    first_name: str | None
    last_name: str | None
    username: str


class Message(BaseModel):
    message_id: int
    chat: Chat
    date: int
    text: str


class Update(BaseModel):
    update_id: int
    message: Message


class GetUpdatesResponse(BaseModel):
    ok: bool
    result: list[Update] = []


class SendMessageResponse(BaseModel):
    ok: bool
    result: Message 
