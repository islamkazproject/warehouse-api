import pytest
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.schemas import OrderCreate, OrderStatus, OrderItemBase
from core.models import Order, OrderItem, Product
from crud.orders import create_order, get_orders, get_order, update_order_status


@pytest.mark.asyncio
async def test_create_order(db_session: AsyncSession):
    product = Product(id=1, name="Test Product", description="Test Product Desc", quantity=100)
    db_session.add(product)
    await db_session.commit()

    order_create = OrderCreate(items=[OrderItemBase(product_id=product.id, quantity=product.quantity)])

    order = await create_order(db_session, order_create)

    assert order is not None
    assert len(order.items) == 1
    assert order.items[0].product_id == 1
    assert order.items[0].quantity == 2
    assert product.quantity == 98


@pytest.mark.asyncio
async def test_get_orders(db_session: AsyncSession):
    product = Product(id=1, name="Test Product", description="Test Product Desc", quantity=100)
    db_session.add(product)
    await db_session.commit()

    order_create = OrderCreate(items=[OrderItemBase(product_id=product.id, quantity=product.quantity)])
    await create_order(db_session, order_create)

    orders = await get_orders(db_session)

    assert len(orders) > 0
    assert orders[0].items[0].product_id == 1


@pytest.mark.asyncio
async def test_get_order(db_session: AsyncSession):
    product = Product(id=1, name="Test Product", description="Test Product Desc", quantity=100)
    db_session.add(product)
    await db_session.commit()

    order_create = OrderCreate(items=[OrderItemBase(product_id=product.id, quantity=product.quantity)])
    order = await create_order(db_session, order_create)

    retrieved_order = await get_order(db_session, order.id)

    assert retrieved_order is not None
    assert retrieved_order.id == order.id


@pytest.mark.asyncio
async def test_update_order_status(db_session: AsyncSession):
    product = Product(id=1, name="Test Product", description="Test Product Desc", quantity=100)
    db_session.add(product)
    await db_session.commit()

    order_create = OrderCreate(items=[OrderItemBase(product_id=product.id, quantity=product.quantity)])
    order = await create_order(db_session, order_create)

    new_status = OrderStatus.send
    updated_order = await update_order_status(db_session, order.id, new_status)

    assert updated_order.status == new_status.name


@pytest.mark.asyncio
async def test_update_order_status_not_found(db_session: AsyncSession):
    with pytest.raises(HTTPException) as exc_info:
        await update_order_status(db_session, 9999, OrderStatus.send)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Order not found"
