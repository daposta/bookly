from fastapi import FastAPI, status
from contextlib import asynccontextmanager
from src.db.main import init_db
from src.books.routes import book_routes
from src.auth.routers import auth_router
from .errors import InvalidToken, UserAlreadyExists, create_exception_handler
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

app.add_exception_handler(
    UserAlreadyExists,
    create_exception_handler(
        status_code=status.HTTP_403_FORBIDDEN,
        initial_detail={
            "message": "User with email already exists",
            "error_code": "user_exists",
        },
    ),
)

app.add_exception_handler(
    InvalidToken,
    create_exception_handler(
        status_code=status.HTTP_403_FORBIDDEN,
        initial_detail={
            "message": "Token is valid or expired ",
            "error_code": "invalid_token",
        },
    ),
)


@app.get("/health-check")
async def get_app_status():
    return {"message": "Application is up"}


app.include_router(book_routes, prefix=f"/api/{version}/books", tags=["books"])
app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=["auth"])
app.include_router(reviews_router, prefix=f"/api/{version}/reviews", tags=["reviews"])
