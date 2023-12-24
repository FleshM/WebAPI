from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from database import Base


class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, unique=True)
    contacts = relationship('Contact', back_populates='group')
    last_update = Column(DateTime(timezone=True), default=datetime.now, onupdate=func.now())


class Contact(Base):
    __tablename__ = 'contacts'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(index=True)
    surname: Mapped[str] = mapped_column(index=True, nullable=True)
    phone: Mapped[str] = mapped_column(index=True)
    email: Mapped[str] = mapped_column(index=True)
    group_id: Mapped[int] = mapped_column(ForeignKey('groups.id'))
    group: Mapped["Group"] = relationship('Group', back_populates='contacts')
    last_update = Column(DateTime(timezone=True), default=datetime.now, onupdate=func.now())
