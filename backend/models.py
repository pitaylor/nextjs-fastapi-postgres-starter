from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import DateTime, Enum, ForeignKey, Index, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import func


class MessageRole(str, PyEnum):
    USER = "user"
    ASSISTANT = "assistant"


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}"


class Thread(Base):
    __tablename__ = "thread"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), index=True)
    name: Mapped[str] = mapped_column(String(255))

    user: Mapped["User"] = relationship("User")

    def __repr__(self) -> str:
        return f"Thread(id={self.id!r}, user_id={self.user_id!r}, name={self.name!r})"


class Message(Base):
    __tablename__ = "message"
    __table_args__ = (Index("ix_message_thread_id_id", "thread_id", "id"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    thread_id: Mapped[int] = mapped_column(ForeignKey("thread.id"), index=True)
    role: Mapped[MessageRole] = mapped_column(Enum(MessageRole))
    content: Mapped[str] = mapped_column(Text)
    sent_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    thread: Mapped["Thread"] = relationship("Thread")

    def __repr__(self) -> str:
        return f"Message(id={self.id!r}, role={self.role!r}, content={self.content[:50]!r}...)"
