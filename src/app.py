from fastapi import FastAPI


from routers import user, friend, party, test


import config

app = FastAPI(**config.metadata)

app.include_router(user.router)
app.include_router(friend.router)
app.include_router(party.router)
app.include_router(test.router)
