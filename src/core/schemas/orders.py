import enum
from datetime import datetime
from typing import List

from pydantic import BaseModel


class OrderStatus(str, enum.Enum):
    in_progress = 'в процессе'
    send = 'отправлено'
    delivered = 'доставлено'


class OrderItemBase(BaseModel):
    product_id: int
    quantity: int


class OrderItemResponse(OrderItemBase):
    id: int


class OrderCreate(BaseModel):
    items: List[OrderItemBase]


class OrderResponse(BaseModel):
    id: int
    created_at: datetime
    status: OrderStatus
    items: List[OrderItemResponse]


class OrderStatusUpdate(BaseModel):
    status: OrderStatus
