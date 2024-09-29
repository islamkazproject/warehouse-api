from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.models import Order, OrderItem, Product
from core.schemas import OrderCreate
from core.schemas.orders import OrderStatus
from utils.products import check_product_availability


async def get_orders(
    session: AsyncSession,
) -> Sequence[Order]:
    statement = select(Order).order_by(Order.id).options(selectinload(Order.items))
    result = await session.execute(statement)
    return result.scalars().all()


async def get_order(
    session: AsyncSession,
    order_id: int
) -> Order:
    statement = select(Order).filter_by(id=order_id)
    result = await session.execute(statement)
    return result.scalars().first()


async def create_order(
    session: AsyncSession,
    order_create: OrderCreate
) -> Order:
    await check_product_availability(session, order_create.items)

    order_items_list = []

    for item in order_create.items:
        statement = select(Product).filter_by(id=item.product_id)
        product = (await session.execute(statement)).scalars().first()

        product.quantity -= item.quantity

        order_item = OrderItem(product_id=item.product_id, quantity=item.quantity)
        order_items_list.append(order_item)

    order = Order()
    order.items.extend(order_items_list)

    return order


async def update_order_status(
    session: AsyncSession,
    order_id: int,
    status: OrderStatus
) -> Order:
    statement = select(Order).filter_by(id=order_id)
    order = (await session.execute(statement)).scalars().first()

    if order.status != status:
        order.status = status.name

    return order
