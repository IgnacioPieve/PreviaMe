from fastapi import FastAPI
from routers import test, party
import config

app = FastAPI(**config.metadata)

app.include_router(party.router)
app.include_router(test.router)


