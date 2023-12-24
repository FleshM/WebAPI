from sqlalchemy.orm import Session

from models import Contact, Group
from routers.contacts import schemas


def create_contact(db: Session, schema: schemas.ContactCreate):
    if db.query(Group).filter_by(id=schema.group_id).first():
        db_contact = Contact(**schema.model_dump())
        db.add(db_contact)
        db.commit()
        db.refresh(db_contact)
        return db_contact
    return False


def get_contact(db: Session, contact_id: int):
    return db.query(Contact).filter_by(id=contact_id).first()


def get_contacts(db: Session):
    return db.query(Contact).all()


def update_contact(db: Session, contact_id: int, contact_data: schemas.ContactUpdate | dict):
    db_contact = db.query(Contact).filter_by(id=contact_id).first()

    contact_data = contact_data if isinstance(contact_data, dict) else contact_data.model_dump()

    if db_contact:
        for key, value in contact_data.items():
            if hasattr(db_contact, key):
                setattr(db_contact, key, value)

        db.commit()
        db.refresh(db_contact)
        return db_contact
    return None


def delete_contact(db: Session, contact_id: int):
    db_contact = db.query(Contact).filter_by(id=contact_id).first()
    if db_contact:
        db.delete(db_contact)
        db.commit()
        return True
    return False
