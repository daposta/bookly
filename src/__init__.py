from fastapi import FastAPI, status
from contextlib import asynccontextmanager

from fastapi.responses import JSONResponse
from src.db.main import init_db
from src.books.routes import book_routes
from src.auth.routers import auth_router
from middleware import register_middleware
from .errors import (
    InvalidRole,
    InvalidToken,
    RefreshTokenRequired,
    UserAlreadyExists,
    create_exception_handler,
    register_all_errors,
)
from src.reviews.routes import reviews_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("server is starting..")
    await init_db()
    yield
    print("server has been stopped")


version = "v1"


app = FastAPI(
    version=version,
    description="A REST API web service for  book reviews",
    title="Bookly",
    # lifespan=lifespan,
)


register_all_errors(app)
register_middleware(app)


@app.get("/health-check")
async def get_app_status():
    return {"message": "Application is up"}


app.include_router(book_routes, prefix=f"/api/{version}/books", tags=["books"])
app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=["auth"])
app.include_router(reviews_router, prefix=f"/api/{version}/reviews", tags=["reviews"])
