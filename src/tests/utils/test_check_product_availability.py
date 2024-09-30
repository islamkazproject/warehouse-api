import pytest
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Product
from core.schemas import OrderItemBase
from utils.products import check_product_availability


@pytest.mark.asyncio
async def test_check_product_availability_success(db_session: AsyncSession):
    product = Product(id=1, name="Test Product", description="Test Product Desc", quantity=100)
    db_session.add(product)
    await db_session.commit()

    items = [OrderItemBase(product_id=1, quantity=5)]

    await check_product_availability(db_session, items)


@pytest.mark.asyncio
async def test_check_product_not_found(db_session: AsyncSession):
    items = [OrderItemBase(product_id=9999, quantity=1)]

    with pytest.raises(HTTPException) as exc_info:
        await check_product_availability(db_session, items)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Product ID 9999 not found"


@pytest.mark.asyncio
async def test_check_product_insufficient_stock(db_session: AsyncSession):
    product = Product(id=1, name="Test Product", description="Test Product Desc", quantity=4)

    db_session.add(product)
    await db_session.commit()

    items = [OrderItemBase(product_id=1, quantity=5)]

    with pytest.raises(HTTPException) as exc_info:
        await check_product_availability(db_session, items)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Not enough stock for product ID 1"
