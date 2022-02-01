from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import get_session
from user.schemas import UserRegistrationIn, UserRegistrationOut
from user import services


auth_router = APIRouter()


@auth_router.post('/registration', response_model=UserRegistrationOut)
async def user_registration(new_user: UserRegistrationIn, session: AsyncSession = Depends(get_session)):
    user = await services.create_user(session=session, new_user=new_user)
    return user