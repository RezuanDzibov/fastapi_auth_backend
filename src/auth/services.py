from uuid import UUID

from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import Verification


async def create_verification(session: AsyncSession, user_id: str):
    statement = insert(Verification).values(user_id=user_id).returning(Verification.id)
    result = await session.execute(statement)
    await session.commit()
    verification = result.scalar()
    return verification