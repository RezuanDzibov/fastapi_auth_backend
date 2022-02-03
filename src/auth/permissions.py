import jwt
from jwt import PyJWTError
from fastapi import Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from starlette.status import HTTP_403_FORBIDDEN
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from src.models.db import get_session
from src.models.user import User
from src.auth.jwt import ALGORITHM
from src.auth.schemas import TokenPayload
from src.user import services as user_services


reusable_oauth2 = OAuth2PasswordBearer(tokenUrl='/login/access-token')


async def get_current_user(token: str = Security(reusable_oauth2), session: AsyncSession = Depends(get_session)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
    except PyJWTError:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )
    user = await user_services.get_user(session=session, where_statements=[User.id == token_data.user_id])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def get_user(current_user: User = Security(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_superuser(current_user: User = Security(get_current_user)):
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user