from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Thread, User


class ThreadService:
    @staticmethod
    async def get_all_threads(session: AsyncSession) -> List[Thread]:
        result = await session.execute(select(Thread))
        return list(result.scalars().all())

    @staticmethod
    async def get_thread_by_id(session: AsyncSession, thread_id: int) -> Thread | None:
        result = await session.execute(select(Thread).where(Thread.id == thread_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def create_thread(session: AsyncSession, user: User, name: str) -> Thread:
        thread = Thread(user_id=user.id, name=name)
        session.add(thread)
        await session.flush()  # Get the thread ID
        return thread

    @classmethod
    async def get_or_create_thread(
        cls: "ThreadService", session: AsyncSession, user: User, thread_id: int | None, content: str
    ) -> Thread | None:
        """
        Get existing thread by ID, or create a new one if thread_id is None.
        Returns None if thread_id is provided and thread is not found.
        """
        if thread_id is None:
            thread_name = content[:30] + ("..." if len(content) > 30 else "")
            return await cls.create_thread(session, user, thread_name)
        else:
            return await cls.get_thread_by_id(session, thread_id)
