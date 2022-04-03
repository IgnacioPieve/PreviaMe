from fastapi import FastAPI
from routers import test
import config

app = FastAPI(**config.metadata)

app.include_router(test.router)


