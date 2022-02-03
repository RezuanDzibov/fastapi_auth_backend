from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import insert, select, delete, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Load

from src.auth.security import verify_password
from src.models.auth import Verification
from src.models.user import User
from src.user import services as user_services


async def authenticate(session: AsyncSession, login: str, password: str):
    statement = select(User).options(
        Load(User).load_only(User.password, User.is_active)
    )
    statement = statement.where(or_(User.username == login, User.email == login))
    result = await session.execute(statement)
    user = result.scalar()
    if user is None:
        raise HTTPException(status_code=404, detail=f'User with username or email: {login}. Not found.')
    if not verify_password(password, user.password):
        raise HTTPException(status_code=400, detail='Provided password is incorrect')
    return user


async def create_verification(session: AsyncSession, user_id: str):
    statement = insert(Verification).values(user_id=user_id).returning(Verification.id)
    result = await session.execute(statement)
    await session.commit()
    verification = result.scalar()
    return verification


async def verify_registration_user(session: AsyncSession, verification_uuid: UUID):
    statement = select(Verification).where(Verification.id == verification_uuid)
    result = await session.execute(statement)
    verification = result.scalar()
    if verification:
        await user_services.update_user(
            session=session, 
            where_statements=[User.id == verification.user_id], 
            to_update={'is_active': True}
        )
        statement = delete(Verification).where(Verification.id == verification_uuid)
        await session.execute(statement)
        await session.commit()
    else:
        raise HTTPException(status_code=404, detail='Not found')