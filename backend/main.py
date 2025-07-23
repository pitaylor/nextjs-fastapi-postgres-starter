from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db_engine import engine
from models import Message, MessageRole, Thread, User
from schemas import MessageCreate, MessageRead, SendMessageResponse, ThreadRead, UserRead
from services.message_service import MessageService
from services.thread_service import ThreadService
from services.user_service import UserService
from seed import seed_thread_if_needed, seed_user_if_needed

seed_user_if_needed()
seed_thread_if_needed()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/users/me")
async def get_my_user():
    async with AsyncSession(engine) as session:
        async with session.begin():
            user = await UserService.get_current_user(session)
            if user is None:
                raise HTTPException(status_code=404, detail="User not found")
            return UserRead(id=user.id, name=user.name)


@app.get("/threads", response_model=List[ThreadRead])
async def get_threads():
    async with AsyncSession(engine) as session:
        async with session.begin():
            threads = await ThreadService.get_all_threads(session)
            return [ThreadRead(id=thread.id, user_id=thread.user_id, name=thread.name) for thread in threads]


@app.get("/threads/{thread_id}/messages", response_model=List[MessageRead])
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


@app.post("/messages", response_model=SendMessageResponse)
async def send_message(message_data: MessageCreate, thread_id: int | None = None):
    async with AsyncSession(engine) as session:
        async with session.begin():
            user = await UserService.get_current_user(session)
            if user is None:
                raise HTTPException(status_code=404, detail="User not found")

            # If no thread_id provided, create a new thread
            if thread_id is None:
                thread_name = message_data.content[:30] + ("..." if len(message_data.content) > 30 else "")
                thread = await ThreadService.create_thread(session, user, thread_name)
            else:
                thread = await ThreadService.get_thread_by_id(session, thread_id)
                if thread is None:
                    raise HTTPException(status_code=404, detail="Thread not found")

            # Create user message
            await MessageService.create_message(session, thread.id, message_data.content, MessageRole.USER)

            # Create mock assistant response
            assistant_content = MessageService.generate_mock_assistant_response(message_data.content)
            assistant_message = await MessageService.create_message(
                session, thread.id, assistant_content, MessageRole.ASSISTANT
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
