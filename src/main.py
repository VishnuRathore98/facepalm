from fastapi import FastAPI
from src.routers.post import router as post_router
from src.routers.comment import router as comment_router
from src.database import database
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)

app.include_router(post_router)
app.include_router(comment_router)


@app.get("/")
async def root():
    return {"message": "facepalm api is running!"}
