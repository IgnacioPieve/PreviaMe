import logging

from fastapi import FastAPI

import config
from routers import friend, manage, party, test, user

logging.basicConfig(filename=".log", encoding="utf-8", level=logging.INFO)
app = FastAPI(**config.metadata)

app.include_router(user.router)
app.include_router(friend.router)
app.include_router(party.router)

app.include_router(manage.router)
app.include_router(test.router)
