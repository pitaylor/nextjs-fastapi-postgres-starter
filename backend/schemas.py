from datetime import datetime

from pydantic import BaseModel

from models import MessageRole


class UserRead(BaseModel):
    id: int
    name: str


class ThreadRead(BaseModel):
    id: int
    user_id: int
    name: str


class MessageRead(BaseModel):
    id: int
    thread_id: int
    content: str
    role: MessageRole
    sent_at: datetime


class MessageCreate(BaseModel):
    content: str


class SendMessageResponse(BaseModel):
    thread: ThreadRead
    message: MessageRead
