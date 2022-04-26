from fastapi import FastAPI

import config
from routers import friend, party, test, user

app = FastAPI(**config.metadata)

app.include_router(user.router)
app.include_router(friend.router)
app.include_router(party.router)
app.include_router(test.router)
