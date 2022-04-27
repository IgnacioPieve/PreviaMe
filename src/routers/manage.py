from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

router = APIRouter(prefix="/manage", tags=["Manage"])


# endpoint to see logs
@router.get("/logs", response_class=PlainTextResponse)
async def get_logs():
    with open(".log", encoding="utf-8") as f:
        return f.read()
