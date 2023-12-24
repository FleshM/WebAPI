from typing import Optional

from pydantic import BaseModel, ConfigDict
from datetime import datetime

from routers.contacts.schemas import Contact


class GroupBase(BaseModel):
    title: str


class GroupCreate(GroupBase):
    pass


class GroupUpdate(GroupBase):
    title: Optional[str] = None


class Group(GroupBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    last_update: datetime
    contacts: list[Contact]
