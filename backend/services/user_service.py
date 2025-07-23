from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import User


class UserService:
    @staticmethod
    async def get_current_user(session: AsyncSession) -> User | None:
        """Get the current user. Since there's only one user in this app, return the first one."""
        result = await session.execute(select(User))
        return result.scalars().first()
