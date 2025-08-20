from datetime import datetime
from uuid import uuid4
from random import choice
from string import ascii_letters, digits
import secrets

from sqlalchemy import DateTime, Integer, String, UUID, Boolean, event, select
from sqlalchemy.orm import Mapped, mapped_column, Session
from sqlalchemy_utils import URLType
from .base import Base

class Url(Base):
    __tablename__ = "urls"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    uuid: Mapped[UUID] = mapped_column(
        String(36),
        nullable=False,
        unique=True,
        index=True,
    )
    url: Mapped[URLType] = mapped_column(URLType, nullable=False)
    short_code: Mapped[str] = mapped_column(String(10), nullable=False, unique=True)
    visit_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.now,
        onupdate=datetime.now,
    )
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=1)


@event.listens_for(Url, "before_insert")
def set_and_validate_uuid(mapper, connection, target):
    session = Session(connection)
    while True:
        uuid = str(uuid4())

        result = session.execute(select(Url).filter(Url.uuid == uuid))
        if not result.scalar_one_or_none():
            target.uuid = uuid
            break


@event.listens_for(Url, "before_insert")
def set_and_validate_short_code(mapper, connection, target):
    session = Session(connection)
    while True:
        alphanumeric_characters = ascii_letters + digits
        size = choice(range(6, 10))
        short_code = "".join(
            secrets.choice(alphanumeric_characters) for _ in range(size)
        )

        result = session.execute(select(Url).filter(Url.short_code == short_code))
        if not result.scalar_one_or_none():
            target.short_code = short_code
            break
