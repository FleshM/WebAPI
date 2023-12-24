import json
from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends

from database import get_db
from sqlalchemy.orm import Session

from routers.groups import schemas, crud
from routers.websocket import websocket_manager

router_groups = APIRouter(prefix='/groups', tags=['group'])


@router_groups.post("/", response_model=schemas.Group)
async def create_group(group_data: schemas.GroupCreate, db: Session = Depends(get_db)):
    group = crud.create_group(db, group_data)
    await websocket_manager.broadcast({
        "type": "notification",
        "message": f"Добавлена новая группа '{group_data.title}'",
        "time": f"{datetime.now()}"
    })
    return group


@router_groups.get("/{group_id}", response_model=schemas.Group)
async def read_group(group_id: int, db: Session = Depends(get_db)):
    group = crud.get_group(db, group_id)
    return group


@router_groups.get("/", response_model=List[schemas.Group])
async def read_groups(db: Session = Depends(get_db)):
    groups = crud.get_groups(db)
    return groups


@router_groups.patch("/{group_id}", response_model=schemas.Group)
async def update_group(group_id: int, group_data: schemas.GroupUpdate, db: Session = Depends(get_db)):
    updated_group = crud.update_group(db, group_id, group_data)
    if updated_group:
        await websocket_manager.broadcast({
            "type": "notification",
            "message": f"Группа ID:{group_id} переименована в '{group_data.title}'",
            "time": f"{datetime.now()}"
        })
        return updated_group
    return {"message": "Группа не найдена"}


@router_groups.delete("/{group_id}")
async def delete_group(group_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_group(db, group_id)
    if deleted:
        await websocket_manager.broadcast({
            "type": "notification",
            "message": f"Группа ID:{group_id} удалена",
            "time": f"{datetime.now()}"
        })
        return {"message": "Группа удалена"}
    return {"message": "Группа не найдена"}
