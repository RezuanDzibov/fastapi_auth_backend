from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.background import BackgroundTasks

from src.auth.jwt import create_token
from src.auth.schemas import Token, Message, OAuth2TokenRequestForm, PasswordResetForm
from src.auth import services as auth_services
from src.models.db import get_session
from src.user.schemas import UserRegistrationIn
from src.user import services as user_services


auth_router = APIRouter()


@auth_router.post('/registration', response_model=Message)
async def user_registration(new_user: UserRegistrationIn, task: BackgroundTasks, session: AsyncSession = Depends(get_session)):
    await user_services.create_user(session=session, new_user=new_user, task=task)
    return Message(message='A verification email has just sent')


@auth_router.post('/login/access-token', response_model=Token)
async def user_access_token(form_data: OAuth2TokenRequestForm = Depends(OAuth2TokenRequestForm.as_form), session: AsyncSession = Depends(get_session)):
    user = await auth_services.authenticate(session=session, login=form_data.login, password=form_data.password)
    if not user.is_active:
        raise HTTPException(status_code=400, detail='Inactive user')
    return create_token(user.id.hex)


@auth_router.get('/confirm-email/{verification_uuid}', response_model=Message)
async def confirm_email(verification_uuid: UUID, session: AsyncSession = Depends(get_session)):
    await auth_services.verify_registration_user(session=session, verification_uuid=verification_uuid)
    return Message(message='Success verify email')


@auth_router.post('/password-recovery/{email}', response_model=Message)
async def recover_password(email: str, task: BackgroundTasks, session: AsyncSession = Depends(get_session)):
    await auth_services.password_recover(session=session, task=task, email=email)
    return Message(message='A recovery email has been sent.')


@auth_router.post('/reset-password', response_model=Message)
async def reset_password(
    form: PasswordResetForm = Depends(PasswordResetForm.as_form),
    session: AsyncSession = Depends(get_session)
):
    await auth_services.reset_password(session=session, token=form.token, new_password=form.new_password)