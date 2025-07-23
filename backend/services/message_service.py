from typing import List, Tuple

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Message, MessageRole, Thread
from services.user_service import UserService


class MessageService:
    @staticmethod
    async def get_messages_by_thread_id(session: AsyncSession, thread_id: int) -> List[Message]:
        result = await session.execute(select(Message).where(Message.thread_id == thread_id))
        return list(result.scalars().all())

    @staticmethod
    async def create_message(session: AsyncSession, thread_id: int, content: str, role: MessageRole) -> Message:
        message = Message(thread_id=thread_id, content=content, role=role)
        session.add(message)
        await session.flush()  # Get the message ID and timestamp
        return message

    @staticmethod
    def generate_mock_assistant_response(user_content: str) -> str:
        return f'I understand you\'re asking about: "{user_content}". This is a response from the assistant.'
