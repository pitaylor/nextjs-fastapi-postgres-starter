from typing import List, Tuple

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Message, MessageRole


class MessageService:
    @staticmethod
    async def get_messages_by_thread_id(session: AsyncSession, thread_id: int) -> List[Message]:
        # Order by ID which reflects insertion order
        result = await session.execute(select(Message).where(Message.thread_id == thread_id).order_by(Message.id))
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

    @classmethod
    async def create_messages_for_interaction(
        cls: "MessageService", session: AsyncSession, thread_id: int, user_content: str
    ) -> Tuple[Message, Message]:
        """Create both user and assistant messages for a complete interaction."""
        user_message = await MessageService.create_message(session, thread_id, user_content, MessageRole.USER)

        assistant_content = MessageService.generate_mock_assistant_response(user_content)
        assistant_message = await MessageService.create_message(
            session, thread_id, assistant_content, MessageRole.ASSISTANT
        )

        return user_message, assistant_message
