from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from database import get_db
from sqlalchemy.orm import Session

from routers.contacts import schemas, crud
from routers.websocket import websocket_manager

router_contacts = APIRouter(prefix='/contacts', tags=['Контакты'])


@router_contacts.post("/", response_model=schemas.Contact, summary='Создание контакта')
async def create_contact(contact_data: schemas.ContactCreate, db: Session = Depends(get_db)):
    contact = crud.create_contact(db, contact_data)
    if not contact:
        return JSONResponse({"message": 'Id группы не найден'}, status_code=404)

    await websocket_manager.broadcast({
        "type": "notification",
        "message": f"В группу '{contact.group.title}' добавлен контакт '{contact.name} {contact.surname}'",
        "time": f"{datetime.now()}"
    })
    return contact


@router_contacts.get("/{contact_id}", response_model=schemas.Contact, summary='Получение контакта')
async def read_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = crud.get_contact(db, contact_id)
    return contact


@router_contacts.get("/", response_model=List[schemas.Contact], summary='Получение контактовы')
async def read_contacts(db: Session = Depends(get_db)):
    contacts = crud.get_contacts(db)
    return contacts


@router_contacts.patch("/{contact_id}", summary='Обновление контакта')
async def update_contact(contact_id: int, contact_data: schemas.ContactUpdate, db: Session = Depends(get_db)):
    updated_contact = crud.update_contact(db, contact_id, contact_data)
    if updated_contact:
        await websocket_manager.broadcast({
            "type": "notification",
            "message": f"Контакт '{updated_contact.name} {updated_contact.surname}' обновлен",
            "time": f"{datetime.now()}"
        })
        return updated_contact
    return {"message": "Контакт не найден"}


@router_contacts.delete("/{contact_id}", summary='Удаление контакта')
async def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_contact(db, contact_id)
    if deleted:
        await websocket_manager.broadcast({
            "type": "notification",
            "message": f"Контакт '{deleted.name} {deleted.surname}' удален",
            "time": f"{datetime.now()}"
        })
        return {"message": "Контакт удален"}
    return {"message": "Контакт не найден"}
