from fastapi import HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..db import get_async_session
from ..models.url import Url


async def pagination(skip: int = 0, limit: int = 10) -> tuple[int, int]:
    return (skip, limit)


async def get_url_or_404(
    short_code: str, session: AsyncSession = Depends(get_async_session)
) -> Url:
    select_query = select(Url).where((Url.short_code == short_code) & Url.active != 0)
    result = await session.execute(select_query)
    # NOTE: scalar_one_or_none -> returns a single object if it exists, or None otherwise
    url = result.scalar_one_or_none()

    if url is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return url
