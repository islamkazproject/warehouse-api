from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models import Base, Product, Order


class OrderItem(Base):
    order_id: Mapped[Optional[int]] = mapped_column(ForeignKey('orders.id', ondelete='SET NULL'))
    product_id: Mapped[Optional[int]] = mapped_column(ForeignKey('products.id', ondelete='SET NULL'))
    quantity: Mapped[int]

    order: Mapped["Order"] = relationship("Order", back_populates="items")
    product: Mapped["Product"] = relationship("Product")


Order.items = relationship("OrderItem", back_populates="order")
