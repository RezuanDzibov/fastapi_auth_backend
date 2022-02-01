from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import or_, select, insert

from base.crud_utils import object_exists
from user.schemas import UserRegistrationIn
from user.models import User


async def create_user(session: AsyncSession, new_user: UserRegistrationIn):
    statement = select(User).where(or_(User.username == new_user.username, User.email == new_user.email))
    is_object_exists = await object_exists(session=session, statement=statement)
    if is_object_exists:
        raise HTTPException(
            status_code=409,
            detail=f'User with username: {new_user.username} or email: {new_user.email} exists'
        )
    statement = insert(User).values(**new_user.dict()).returning('*')
    result = await session.execute(statement)
    await session.commit()
    user = result.one()
    return user