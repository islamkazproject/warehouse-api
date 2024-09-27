import enum
from datetime import datetime

from sqlalchemy import text
from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from core.models import Base


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
    status: Mapped[OrderStatus] = mapped_column(default=OrderStatus.in_progress)
