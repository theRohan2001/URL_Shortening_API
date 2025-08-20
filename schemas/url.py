from datetime import datetime
from pydantic import BaseModel, Field, AnyHttpUrl


class UrlBase(BaseModel):
    url: AnyHttpUrl

    class Config:
        from_attributes = True


class UrlCreate(UrlBase):
    short_code: str | None = None


class UrlUpdate(BaseModel):
    url: str | None = None


class UrlRead(UrlBase):
    id: int
    uuid: str
    short_code: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class UrlStats(UrlBase):
    id: int
    uuid: str
    short_code: str
    visit_count: int
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    active: bool
