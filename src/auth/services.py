from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import insert, select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.auth import Verification
from src.user import services as user_services


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
        await user_services.update_user(session=session, user_id=verification.user_id, to_update={'is_active': True})
        statement = delete(Verification).where(Verification.id == verification_uuid)
        await session.execute(statement)
        await session.commit()
    else:
        raise HTTPException(status_code=404, detail='Not found')