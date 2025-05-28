from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.db.main import init_db
from src.books.routes import book_routes
from src.auth.routers import auth_router


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


@app.get("/health-check")
async def get_app_status():
    return {"message": "Application is up"}


app.include_router(book_routes, prefix=f"/api/{version}/books", tags=["books"])
app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=["auth"])
