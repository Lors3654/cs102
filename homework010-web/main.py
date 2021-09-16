import uvicorn  # type:ignore
from fastapi import FastAPI  # type:ignore

from models.database import database
from routers import notes, users

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(users.router)
app.include_router(notes.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
