from datetime import datetime
from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db_engine import engine
from models import Message, MessageRole, Thread, User
from seed import seed_thread_if_needed, seed_user_if_needed

# TODO: refactor into separate files (if it makes sense)

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


@app.get("/users/me")
async def get_my_user():
    async with AsyncSession(engine) as session:
        async with session.begin():
            # Sample logic to simplify getting the current user. There's only one user.
            result = await session.execute(select(User))
            user = result.scalars().first()

            if user is None:
                raise HTTPException(status_code=404, detail="User not found")
            return UserRead(id=user.id, name=user.name)


@app.get("/threads", response_model=List[ThreadRead])
async def get_threads():
    async with AsyncSession(engine) as session:
        async with session.begin():
            result = await session.execute(select(Thread))
            threads = result.scalars().all()
            return [ThreadRead(id=thread.id, user_id=thread.user_id, name=thread.name) for thread in threads]


@app.get("/threads/{thread_id}/messages", response_model=List[MessageRead])
async def get_messages(thread_id: int):
    async with AsyncSession(engine) as session:
        async with session.begin():
            # Check if thread exists
            thread_result = await session.execute(select(Thread).where(Thread.id == thread_id))
            thread = thread_result.scalar_one_or_none()
            if thread is None:
                raise HTTPException(status_code=404, detail="Thread not found")

            # Get messages for the thread
            result = await session.execute(select(Message).where(Message.thread_id == thread_id))
            messages = result.scalars().all()
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
            user_result = await session.execute(select(User))
            user = user_result.scalar_one_or_none()
            if user is None:
                raise HTTPException(status_code=404, detail="User not found")

            # If no thread_id provided, create a new thread
            if thread_id is None:
                thread_name = message_data.content[:30] + ("..." if len(message_data.content) > 30 else "")
                new_thread = Thread(user_id=user.id, name=thread_name)
                session.add(new_thread)
                await session.flush()  # Get the thread ID
                thread = new_thread
            else:
                thread_result = await session.execute(select(Thread).where(Thread.id == thread_id))
                thread = thread_result.scalar_one_or_none()
                if thread is None:
                    raise HTTPException(status_code=404, detail="Thread not found")

            # Create user message
            user_message = Message(thread_id=thread.id, content=message_data.content, role=MessageRole.USER)
            session.add(user_message)
            await session.flush()

            # Create mock assistant response
            assistant_content = (
                f'I understand you\'re asking about: "{message_data.content}". This is a response from the assistant.'
            )
            assistant_message = Message(
                thread_id=thread.id,
                content=assistant_content,
                role=MessageRole.ASSISTANT,
            )
            session.add(assistant_message)
            await session.flush()

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
