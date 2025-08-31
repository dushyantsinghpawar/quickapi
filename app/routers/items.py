from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..db import get_db
from ..security import get_current_user

router = APIRouter(prefix="/items", tags=["items"])


@router.post("", response_model=schemas.ItemOut, status_code=201)
def create_item(
    payload: schemas.ItemCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    obj = models.Item(name=payload.name, description=payload.description)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("", response_model=list[schemas.ItemOut])
def list_items(
    q: str | None = None,
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db),
):
    query = db.query(models.Item)
    if q:
        query = query.filter(models.Item.name.ilike(f"%{q}%"))
    return query.order_by(models.Item.id.desc()).offset(offset).limit(limit).all()


@router.get("/{item_id}", response_model=schemas.ItemOut)
def get_item(item_id: int, db: Session = Depends(get_db)):
    obj = db.get(models.Item, item_id)
    if not obj:
        raise HTTPException(404, "Item not found")
    return obj


@router.put("/{item_id}", response_model=schemas.ItemOut)
def update_item(
    item_id: int,
    payload: schemas.ItemCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    obj = db.get(models.Item, item_id)
    if not obj:
        raise HTTPException(404, "Item not found")
    obj.name = payload.name
    obj.description = payload.description
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{item_id}", status_code=204)
def delete_item(
    item_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    obj = db.get(models.Item, item_id)
    if not obj:
        raise HTTPException(404, "Item not found")
    db.delete(obj)
    db.commit()
    return
