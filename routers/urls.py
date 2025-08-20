from fastapi import APIRouter, status, Depends
from sqlalchemy.engine import Result
from sqlalchemy import select, Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import get_async_session
from ..schemas.url import UrlCreate, UrlRead, UrlUpdate, UrlStats
from ..models.url import Url

from ..helpers.endpoint import pagination, get_url_or_404

router = APIRouter(
    prefix="/shorten",
    tags=["urls"],
)


# Create Short URL
@router.post("/", response_model=UrlRead, status_code=status.HTTP_201_CREATED)
async def create_url(
    new_url: UrlCreate, session: AsyncSession = Depends(get_async_session)
) -> Url:
    url = Url(url=str(new_url.url))
    session.add(url)
    await session.commit()

    return url


# Retrieve Original URL
@router.get("/{short_code}", response_model=UrlRead, status_code=status.HTTP_200_OK)
async def get_url(short_code: str, url: Url = Depends(get_url_or_404)) -> Url:
    return url


# Get All URLs
@router.get("/", response_model=list[UrlRead])
async def get_urls(
    pagination: tuple[int, int] = Depends(pagination),
    session: AsyncSession = Depends(get_async_session),
) -> Sequence[Url]:
    skip, limit = pagination
    select_query = select(Url).offset(skip).limit(limit)

    result : Result = await session.execute(select_query)

    urls = result.scalars(Url).all()

    return urls


# Update Original URL
@router.put("/{short_code}", response_model=UrlRead, status_code=status.HTTP_200_OK)
async def update_url(
    short_code: str,
    updated_url: UrlUpdate,
    url: Url = Depends(get_url_or_404),
    session: AsyncSession = Depends(get_async_session),
) -> Url:
    url_update_dict = updated_url.model_dump(exclude_unset=True)
    for key, value in url_update_dict.items():
        setattr(url, key, value)

    session.add(url)
    await session.commit()

    return url


# Delete URL record
@router.delete("/{short_code}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_url(
    short_code: str,
    url: Url = Depends(get_url_or_404),
    session: AsyncSession = Depends(get_async_session),
):
    await session.delete(url)
    await session.commit()


# Deactivate URL record
@router.patch("/{short_code}", status_code=status.HTTP_204_NO_CONTENT)
async def deactivate_url(
    short_code: str,
    url: Url = Depends(get_url_or_404),
    session: AsyncSession = Depends(get_async_session),
) -> None:
    url.active = False

    session.add(url)
    await session.commit()

    return None


# Get URL stats
@router.get(
    "/{short_code}/stats", response_model=UrlStats, status_code=status.HTTP_200_OK
)
async def get_url_stats(
    short_code: str,
    url: Url = Depends(get_url_or_404),
) -> Url:
    return url
