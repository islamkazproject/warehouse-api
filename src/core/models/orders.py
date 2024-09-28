import enum
from datetime import datetime
from typing import Optional

from sqlalchemy import Enum as SQLAEnum
from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models import Base, Product


class OrderStatus(enum.Enum):
    in_progress = 'в процессе'
    send = 'отправлено'
    delivered = 'доставлено'


class Order(Base):
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.utcnow,
    )
    status: Mapped[OrderStatus] = mapped_column(SQLAEnum(OrderStatus), default=OrderStatus.in_progress)
    items: Mapped[list["OrderItem"]] = relationship("OrderItem", back_populates="order", lazy='selectin')


class OrderItem(Base):
    order_id: Mapped[Optional[int]] = mapped_column(ForeignKey('orders.id', ondelete='SET NULL'))
    product_id: Mapped[Optional[int]] = mapped_column(ForeignKey('products.id', ondelete='SET NULL'))
    quantity: Mapped[int]

    order: Mapped["Order"] = relationship("Order", back_populates="items")
    product: Mapped["Product"] = relationship("Product")
