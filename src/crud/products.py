from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Product
from core.schemas import ProductCreate, ProductRetrieve, ProductUpdate


async def get_products(
    session: AsyncSession,
) -> Sequence[Product]:
    statement = select(Product).order_by(Product.id)
    result = await session.scalars(statement)
    return result.all()


async def get_product(
    session: AsyncSession,
    product_id: int
) -> Product:
    statement = select(Product).filter_by(id=product_id)
    result = await session.scalars(statement)
    return result.first()


async def update_product(
    session: AsyncSession,
    product_id: int,
    product: ProductUpdate
) -> Product:
    statement = select(Product).filter_by(id=product_id)
    result = await session.scalars(statement)
    updated_product = result.first()

    for key, value in product.dict(exclude_unset=True).items():
        setattr(updated_product, key, value)

    await session.commit()
    await session.refresh(updated_product)
    return updated_product


async def create_product(
    session: AsyncSession,
    product_create: ProductCreate,
) -> Product:
    product = Product(**product_create.model_dump())
    session.add(product)
    await session.commit()
    await session.refresh(product)
    return product
