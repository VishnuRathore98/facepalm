from fastapi import FastAPI
from src.routers.post import router as post_router
from src.routers.comment import router as comment_router

app = FastAPI()

app.include_router(post_router)
app.include_router(comment_router)


@app.get("/")
async def root():
    return {"message": "facepalm api is running!"}
