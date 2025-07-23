from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import messages, threads, users
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

app.include_router(users.router)
app.include_router(threads.router)
app.include_router(messages.router)
