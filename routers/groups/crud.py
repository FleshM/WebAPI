from sqlalchemy.orm import Session

from models import Group
from routers.groups import schemas


def create_group(db: Session, schema: schemas.GroupCreate):
    db_group = Group(**schema.model_dump())
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group


def get_group(db: Session, group_id: int):
    return db.query(Group).filter_by(id=group_id).first()


def get_groups(db: Session):
    return db.query(Group).all()


def update_group(db: Session, group_id: int, group_data: schemas.GroupUpdate | dict):
    db_group = db.query(Group).filter_by(id=group_id).first()

    group_data = group_data if isinstance(group_data, dict) else group_data.model_dump()

    if db_group:
        for key, value in group_data.items():
            if hasattr(db_group, key):
                setattr(db_group, key, value)

        db.commit()
        db.refresh(db_group)

    return db_group


def delete_group(db: Session, group_id: int):
    db_group = db.query(Group).filter_by(id=group_id).first()
    if db_group:
        db.delete(db_group)
        db.commit()
        return True
    return False

