from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from auth.jwt import create_token
from auth.schemas import Token
from core.db import get_session
from user.schemas import UserRegistrationIn
from user import services


auth_router = APIRouter()


@auth_router.post('/registration')
async def user_registration(new_user: UserRegistrationIn, session: AsyncSession = Depends(get_session)):
    await services.create_user(session=session, new_user=new_user)
    return


@auth_router.post('/login/access-token', response_model=Token)
async def user_access_token(form_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_session)):
    user = await services.authenticate(session=session, username=form_data.username, password=form_data.password)
    if not user.is_active:
        raise HTTPException(status_code=400, detail='Inactive user')
    return create_token(user.id.hex)