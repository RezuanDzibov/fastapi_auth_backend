from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID

from fastapi import BackgroundTasks, HTTPException
import jwt
from sqlalchemy import insert, select, delete, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Load
from config import settings
from src.auth.jwt import ALGORITHM

from src.auth.security import get_password_hash, verify_password
from src.auth.send_email import send_reset_password_email
from src.models.auth import Verification
from src.models.user import User
from src.user import services as user_services


password_reset_jwt_subject = 'preset'


async def authenticate(session: AsyncSession, login: str, password: str):
    statement = select(User).options( # type: ignore
        Load(User).load_only(User.password, User.is_active) # type: ignore
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


async def password_recover(session: AsyncSession, task: BackgroundTasks, email: str):
    user = await user_services.get_user(session=session, where_statements=[User.email == email])
    if not user:
        raise HTTPException(
            status_code=404,
            detail=f'The user with this email: {email} does not exist in the system.',
        )
    password_reset_token = await generate_password_reset_token(email)
    task.add_task(
        send_reset_password_email, email_to=user.email, email=email, token=password_reset_token
    )


async def generate_password_reset_token(email: str):
    delta = timedelta(minutes=settings.EMAIL_RESET_TOKEN_EXPIRE)
    now = datetime.utcnow()
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {'exp': exp, 'nbf': now, 'sub': password_reset_jwt_subject, 'email': email},
        settings.SECRET_KEY,
        algorithm=ALGORITHM,
    )
    return encoded_jwt


async def verify_password_reset_token(token: str) -> Optional[str]:
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        assert decoded_token['sub'] == password_reset_jwt_subject
        return decoded_token['email']
    except jwt.InvalidTokenError:
        return None
    
    
async def reset_password(session: AsyncSession, token: str, new_password: str):
    email = await verify_password_reset_token(token)
    if not email:
        raise HTTPException(status_code=400, detail='Invalid token')
    user = await user_services.get_user(session=session, where_statements=[User.email == email])
    if not user:
        raise HTTPException(
            status_code=404,
            detail=f'The user with this email: {email} does not exist in the system.',
        )
    elif not user.is_active:
        raise HTTPException(status_code=400, detail='Inactive user')
    password_hash = get_password_hash(new_password)
    await user_services.update_user(
        session=session, 
        where_statements=[User.id == user.id],
        to_update={'password': password_hash}
    )