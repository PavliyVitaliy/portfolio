from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User
from core.config import settings


async def get_super_user(
    session: AsyncSession,
) -> User:
    super_user = settings.super_user.email
    stmt = select(User).where(User.email == super_user)
    result = await session.scalars(stmt)
    return result.one()
