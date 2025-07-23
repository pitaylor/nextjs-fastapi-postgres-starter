from typing import List

from fastapi import APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from db_engine import engine
from schemas import MessageRead, ThreadRead
from services.message_service import MessageService
from services.thread_service import ThreadService

router = APIRouter(prefix="/threads", tags=["threads"])


@router.get("/", response_model=List[ThreadRead])
async def get_threads():
    async with AsyncSession(engine) as session:
        async with session.begin():
            threads = await ThreadService.get_all_threads(session)
            return [ThreadRead(id=thread.id, user_id=thread.user_id, name=thread.name) for thread in threads]


@router.get("/{thread_id}/messages", response_model=List[MessageRead])
async def get_messages(thread_id: int):
    async with AsyncSession(engine) as session:
        async with session.begin():
            # Check if thread exists
            thread = await ThreadService.get_thread_by_id(session, thread_id)
            if thread is None:
                raise HTTPException(status_code=404, detail="Thread not found")

            # Get messages for the thread
            messages = await MessageService.get_messages_by_thread_id(session, thread_id)
            return [
                MessageRead(
                    id=message.id,
                    thread_id=message.thread_id,
                    content=message.content,
                    role=message.role,
                    sent_at=message.sent_at,
                )
                for message in messages
            ]