import pytest
from fastapi import HTTPException
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from core.schemas import OrderCreate, OrderStatus, OrderItemBase
from core.models import Order, OrderItem, Product
from crud.orders import create_order


@pytest.mark.asyncio
async def test_post_create_order(db_session: AsyncSession, ac: AsyncClient):
    product = Product(id=1, name="Test Product", description="Test Product Desc", quantity=100)
    db_session.add(product)
    await db_session.commit()

    order_data = OrderCreate(items=[OrderItemBase(product_id=product.id, quantity=product.quantity)])

    response = await ac.post("/api/v1/orders", json=order_data.model_dump(mode='json'))

    assert response.status_code == 201
    order = response.json()
    assert order["items"][0]["product_id"] == 1
    assert order["items"][0]["quantity"] == 2


@pytest.mark.asyncio
async def test_get_list_orders(db_session: AsyncSession, ac: AsyncClient):
    product = Product(id=1, name="Test Product", description="Test Product Desc", quantity=100)
    db_session.add(product)
    await db_session.commit()

    order_data = OrderCreate(items=[OrderItemBase(product_id=product.id, quantity=product.quantity)])

    await create_order(db_session, order_data)

    response = await ac.get("/api/v1/orders")

    assert response.status_code == 200
    orders = response.json()
    assert len(orders) > 0


@pytest.mark.asyncio
async def test_get_retrieve_order(db_session: AsyncSession, ac: AsyncClient):
    product = Product(id=1, name="Test Product", description="Test Product Desc", quantity=100)
    db_session.add(product)
    await db_session.commit()

    order_data = OrderCreate(items=[OrderItemBase(product_id=product.id, quantity=product.quantity)])

    order = await create_order(db_session, order_data)

    response = await ac.get(f"/api/v1/orders/{order.id}")

    assert response.status_code == 200
    order_response = response.json()
    assert order_response["id"] == order.id


@pytest.mark.asyncio
async def test_patch_order_status(db_session: AsyncSession, ac: AsyncClient):
    product = Product(id=1, name="Test Product", description="Test Product Desc", quantity=100)
    db_session.add(product)
    await db_session.commit()

    order_data = OrderCreate(items=[OrderItemBase(product_id=product.id, quantity=product.quantity)])

    order = await create_order(db_session, order_data)

    new_status = OrderStatus.send
    response = await ac.patch(f"/api/v1/orders/{order.id}/status", json={"status": new_status.name})

    assert response.status_code == 200
    updated_order = response.json()
    assert updated_order["status"] == new_status.name


@pytest.mark.asyncio
async def test_get_order_not_found(db_session: AsyncSession, ac: AsyncClient):
    response = await ac.get("/api/v1/orders/9999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Order not found"
