from fastapi import APIRouter, Depends, status
from order.controller import OrderController
from order.schemas import OrderInSchema, OrderSchema, OrderUpdateSchema
from sqlalchemy.orm import Session
from utils import get_db
from typing import List

router = APIRouter()


@router.get("/", response_model=List[OrderSchema])
def get_orders(db: Session = Depends(get_db)):
    """
    Get all orders
    """
    return OrderController.get_all(db)


@router.get("/user/{user_id}", response_model=List[OrderSchema])
def get_orders_by_user(user_id: int, db: Session = Depends(get_db)):
    """
    Get all orders
    """
    return OrderController.get_by_user_id(db, user_id)


@router.get("/{id}", response_model=OrderSchema)
def get_order(id: int, db: Session = Depends(get_db)):
    """
    Get order by id
    """
    return OrderController.get_by_id(db, id)


@router.post("/", response_model=OrderSchema, status_code=status.HTTP_201_CREATED)
def create_order(order: OrderInSchema, db: Session = Depends(get_db)):
    """
    Create new order
    """
    return OrderController.create(db, order)


@router.put("/", response_model=OrderSchema)
def update_order(order: OrderUpdateSchema, db: Session = Depends(get_db)):
    """
    Update order
    """
    return OrderController.update(db, order)


@router.delete("/{id}", response_model=OrderSchema)
def delete_order(id: int, db: Session = Depends(get_db)):
    """
    Delete order
    """
    return OrderController.delete(db, id)

