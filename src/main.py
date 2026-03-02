from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.database import async_main
from src.api import main_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await async_main()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(main_router)