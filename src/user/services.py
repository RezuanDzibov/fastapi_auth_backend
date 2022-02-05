from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import or_, select
from starlette.background import BackgroundTasks

from src.auth.security import get_password_hash
from src.auth.send_email import send_new_account_email
from src.auth import services as auth_services
from src.base import crud_utils
from src.base.crud_utils import object_exists
from src.user.schemas import UserRegistrationIn
from src.models.user import User


async def create_user(session: AsyncSession, new_user: UserRegistrationIn, task: BackgroundTasks):
    statement = select(User).where(or_(User.username == new_user.username, User.email == new_user.email))
    is_object_exists = await object_exists(session=session, statement=statement)
    if is_object_exists:
        raise HTTPException(
            status_code=409,
            detail=f'User with username: {new_user.username} or email: {new_user.email} exists'
        )
    raw_password = new_user.dict().pop('password')
    hash_password = get_password_hash(raw_password)
    new_user.password = hash_password
    user = await crud_utils.insert_object(session=session, model=User, to_insert=new_user.dict(), returning=[User.id])
    verification = await auth_services.create_verification(session=session, user_id=str(user))
    task.add_task(
        send_new_account_email, new_user.email, new_user.username, raw_password, verification
    )


async def get_user(session: AsyncSession, where_statements: list):
    statement = select(User).where(*where_statements)
    user = await crud_utils.get_object(session=session, statement=statement)
    return user


async def update_user(session: AsyncSession, where_statements: list, to_update: dict, returning: list):
    user = await crud_utils.update_object(
        session=session,
        model=User,
        where_statements=where_statements,
        to_update=to_update,
        returning=returning
    )
    return user