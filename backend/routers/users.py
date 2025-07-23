from fastapi import APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from db_engine import engine
from schemas import UserRead
from services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me")
async def get_my_user():
    async with AsyncSession(engine) as session:
        async with session.begin():
            user = await UserService.get_current_user(session)
            if user is None:
                raise HTTPException(status_code=404, detail="User not found")
            return UserRead(id=user.id, name=user.name)
