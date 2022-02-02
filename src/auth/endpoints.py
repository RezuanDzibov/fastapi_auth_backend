from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.background import BackgroundTasks

from src.auth.jwt import create_token
from src.auth.schemas import Token, Message
from src.models.db import get_session
from src.user.schemas import UserRegistrationIn
from src.user import services


auth_router = APIRouter()


@auth_router.post('/registration', response_model=Message)
async def user_registration(new_user: UserRegistrationIn, task: BackgroundTasks, session: AsyncSession = Depends(get_session)):
    await services.create_user(session=session, new_user=new_user, task=task)
    return Message(message='A verification email has just sent')


@auth_router.post('/login/access-token', response_model=Token)
async def user_access_token(form_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_session)):
    user = await services.authenticate(session=session, username=form_data.username, password=form_data.password)
    if not user.is_active:
        raise HTTPException(status_code=400, detail='Inactive user')
    return create_token(user.id.hex)