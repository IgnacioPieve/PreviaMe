import datetime
import traceback

from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response

import config
from database import db
from routers import friend, party, test, user

app = FastAPI(**config.metadata)

app.include_router(user.router)
app.include_router(friend.router)
app.include_router(party.router)
app.include_router(test.router)


async def log_request(request: Request, call_next):
    try:
        response = await call_next(request)
        await db["log"].insert_one(
            {
                "success": True,
                "date": datetime.datetime.now(),
                "url": str(request.url),
                "method": request.method,
                "headers": dict(request.headers),
            }
        )
        return response

    except Exception as e:
        await db["log"].insert_one(
            {
                "success": False,
                "date": datetime.datetime.now(),
                "url": str(request.url),
                "method": request.method,
                "headers": dict(request.headers),
                "error": str(traceback.format_exc()),
            }
        )
        raise e


db["log"].create_index([("date", 1)])
app.middleware("http")(log_request)
