from fastapi import APIRouter

from src.auth.endpoints import auth_router


routes = APIRouter()


routes.include_router(auth_router, prefix='/auth', tags=['auth'])