from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import get_session
from user.schemas import UserRegistrationIn
from user import services


auth_router = APIRouter()


@auth_router.post('/registration')
async def user_registration(new_user: UserRegistrationIn, session: AsyncSession = Depends(get_session)):
    await services.create_user(session=session, new_user=new_user)
    return