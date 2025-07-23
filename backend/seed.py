from sqlalchemy import select
from sqlalchemy.orm import Session
from db_engine import sync_engine
from models import User, Thread, Message, MessageRole


def seed_user_if_needed():
    with Session(sync_engine) as session:
        with session.begin():
            if session.execute(select(User)).scalar_one_or_none() is not None:
                print("User already exists, skipping seeding")
                return
            print("Seeding user")
            session.add(User(name="Alice"))
            session.commit()


def seed_thread_if_needed():
    with Session(sync_engine) as session:
        with session.begin():
            if session.execute(select(Thread)).scalars().first() is not None:
                print("Thread already exists, skipping seeding")
                return

            user = session.execute(select(User)).scalar_one_or_none()
            if user is None:
                print("No user found, cannot create thread")
                return

            print("Seeding sample thread")
            thread = Thread(user_id=user.id, name="Sample Chat")
            session.add(thread)
            session.flush()
            session.add(
                Message(
                    thread_id=thread.id, role=MessageRole.ASSISTANT, content="Hi there?"
                )
            )
            session.commit()
