from typing import Optional

from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime


class ContactBase(BaseModel):
    name: str
    surname: str
    phone: str
    email: str
    group_id: int


class ContactCreate(ContactBase):
    pass


class ContactUpdate(ContactBase):
    name: Optional[str] = None
    surname: Optional[str] = None
    phone:  Optional[str] = None
    email: Optional[str] = None
    group_id: Optional[int] = None


class Contact(ContactBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    last_update: datetime
