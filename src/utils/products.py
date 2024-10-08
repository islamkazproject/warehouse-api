from typing import List

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Product
from core.schemas import OrderItemBase


async def check_product_availability(
    session: AsyncSession,
    items: List[OrderItemBase]
) -> None:
    for item in items:
        statement = select(Product).filter_by(id=item.product_id)
        product = (await session.execute(statement)).scalars().first()

        if not product:
            raise HTTPException(status_code=404, detail=f"Product ID {item.product_id} not found")

        if product.quantity < item.quantity:
            raise HTTPException(status_code=400, detail=f"Not enough stock for product ID {item.product_id}")
