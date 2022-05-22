from sqlalchemy.orm import Session
from exception import not_found_404
from order.schemas import OrderSchema, OrderInSchema, OrderUpdateSchema
from order.models import Order


class OrderController:
    @staticmethod
    def create(db: Session, order: OrderInSchema):
        _o = Order(**order.dict())
        db.add(_o)
        db.commit()
        db.refresh(_o)
        return _o

    @staticmethod
    def get_all(db: Session):
        return db.query(Order).all()

    @staticmethod
    def get_by_id(db: Session, id: int):
        _o = db.query(Order).filter(Order.id == id).first()
        if _o:
            return _o
        raise not_found_404

    @staticmethod
    def delete(db: Session, id: int):
        _o = OrderController.get_by_id(db, id)
        db.delete(_o)
        db.commit()
        return _o

    @staticmethod
    def update(db: Session, order: OrderUpdateSchema):
        print(order)
        _o = OrderController.get_by_id(db, order.id)
        for key, value in order.dict().items():
            if key != 'id':
                setattr(_o, key, value)
        db.commit()
        return _o

    @staticmethod
    def get_by_user_id(db: Session, user_id: int):
        return db.query(Order).filter(Order.user_id == user_id).all()
