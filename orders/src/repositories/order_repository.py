from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from entities.order import Order, OrderCreate, OrderUpdate, OrderStatus
from repositories.interfaces.order_repository import OrderRepository as OrderRepositoryInterface
from entities.database_models import Order as OrderModel

class OrderRepository(OrderRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def create(self, order_data: OrderCreate) -> Order:
        db_order = OrderModel(
            customer_name=order_data.customer_name,
            customer_email=order_data.customer_email,
            customer_phone=order_data.customer_phone,
            pickup_address=order_data.pickup_address,
            delivery_address=order_data.delivery_address,
            cargo_type=order_data.cargo_type,
            cargo_weight=order_data.cargo_weight,
            cargo_volume=order_data.cargo_volume,
            notes=order_data.notes,
            status=OrderStatus.PENDING.value
        )
        self.db.add(db_order)
        self.db.commit()
        self.db.refresh(db_order)
        return self._to_entity(db_order)

    def get_by_id(self, order_id: str) -> Optional[Order]:
        db_order = self.db.query(OrderModel).filter(OrderModel.id == order_id).first()
        return self._to_entity(db_order) if db_order else None

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Order]:
        db_orders = self.db.query(OrderModel).offset(skip).limit(limit).all()
        return [self._to_entity(o) for o in db_orders]

    def update(self, order_id: str, order_data: OrderUpdate) -> Optional[Order]:
        db_order = self.db.query(OrderModel).filter(OrderModel.id == order_id).first()
        if not db_order:
            return None
        for field, value in order_data.dict(exclude_unset=True).items():
            setattr(db_order, field, value)
        self.db.commit()
        self.db.refresh(db_order)
        return self._to_entity(db_order)

    def delete(self, order_id: str) -> bool:
        db_order = self.db.query(OrderModel).filter(OrderModel.id == order_id).first()
        if not db_order:
            return False
        self.db.delete(db_order)
        self.db.commit()
        return True

    def get_by_status(self, status: str) -> List[Order]:
        db_orders = self.db.query(OrderModel).filter(OrderModel.status == status).all()
        return [self._to_entity(o) for o in db_orders]

    def get_by_customer_email(self, email: str) -> List[Order]:
        db_orders = self.db.query(OrderModel).filter(OrderModel.customer_email == email).all()
        return [self._to_entity(o) for o in db_orders]

    def _to_entity(self, db_order: OrderModel) -> Order:
        return Order(
            id=db_order.id,
            customer_name=db_order.customer_name,
            customer_email=db_order.customer_email,
            customer_phone=db_order.customer_phone,
            pickup_address=db_order.pickup_address,
            delivery_address=db_order.delivery_address,
            cargo_type=db_order.cargo_type,
            cargo_weight=db_order.cargo_weight,
            cargo_volume=db_order.cargo_volume,
            status=OrderStatus(db_order.status),
            vehicle_id=db_order.vehicle_id,
            driver_id=db_order.driver_id,
            estimated_cost=db_order.estimated_cost,
            actual_cost=db_order.actual_cost,
            pickup_date=db_order.pickup_date,
            delivery_date=db_order.delivery_date,
            notes=db_order.notes,
            created_at=db_order.created_at,
            updated_at=db_order.updated_at
        ) 