from fastapi import FastAPI, HTTPException
from fastapi.exception_handlers import http_exception_handler
from routers.post import router as post_router
from routers.comment import router as comment_router
from routers.user import router as user_router
from database import database
from contextlib import asynccontextmanager
from logging_conf import configure_logging
from asgi_correlation_id import CorrelationIdMiddleware
import logging


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await configure_logging()
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)

app.add_middleware(CorrelationIdMiddleware)

app.include_router(post_router)
app.include_router(comment_router)
app.include_router(user_router)


@app.get("/")
async def root():
    return {"message": "facepalm api is running!"}


# this will give us detailed logs related to HTTPExceptions, we are
# overwriting the HTTPException.
@app.exception_handler(HTTPException)
async def logging_http_exception_handler(request, exception):
    logger.error(f"HTTPException: {exception.status_code} {exception.detail}")
    return await http_exception_handler(request, exception)
