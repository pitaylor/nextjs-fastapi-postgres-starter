from sqlalchemy import String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from datetime import datetime
from enum import Enum as PyEnum


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
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    name: Mapped[str] = mapped_column(String(255))

    user: Mapped["User"] = relationship("User")

    def __repr__(self) -> str:
        return f"Thread(id={self.id!r}, user_id={self.user_id!r}, name={self.name!r})"


class Message(Base):
    __tablename__ = "message"

    id: Mapped[int] = mapped_column(primary_key=True)
    thread_id: Mapped[int] = mapped_column(ForeignKey("thread.id"))
    role: Mapped[MessageRole] = mapped_column(Enum(MessageRole))
    content: Mapped[str] = mapped_column(Text)

    # todo: fix this deprecation warning
    sent_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    thread: Mapped["Thread"] = relationship("Thread")

    def __repr__(self) -> str:
        return f"Message(id={self.id!r}, role={self.role!r}, content={self.content[:50]!r}...)"
