from fastapi import APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from db_engine import engine
from schemas import MessageCreate, MessageRead, SendMessageResponse, ThreadRead
from services.message_service import MessageService
from services.thread_service import ThreadService
from services.user_service import UserService

router = APIRouter(prefix="/messages", tags=["messages"])


@router.post("/", response_model=SendMessageResponse)
async def send_message(message_data: MessageCreate, thread_id: int | None = None):
    async with AsyncSession(engine) as session:
        async with session.begin():
            user = await UserService.get_current_user(session)
            if user is None:
                raise HTTPException(status_code=404, detail="User not found")

            # Get existing thread or create new one
            thread = await ThreadService.get_or_create_thread(session, user, thread_id, message_data.content)
            if thread is None:
                raise HTTPException(status_code=404, detail="Thread not found")

            # Create user and assistant messages for the interaction
            _, assistant_message = await MessageService.create_messages_for_interaction(
                session, thread.id, message_data.content
            )

            response = SendMessageResponse(
                thread=ThreadRead(id=thread.id, user_id=thread.user_id, name=thread.name),
                message=MessageRead(
                    id=assistant_message.id,
                    thread_id=assistant_message.thread_id,
                    content=assistant_message.content,
                    role=assistant_message.role,
                    sent_at=assistant_message.sent_at,
                ),
            )

            await session.commit()

            return response