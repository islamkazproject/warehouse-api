from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Product
from core.schemas import ProductRetrieve, ProductCreate
from crud.products import list_products, create_product, retrieve_product
from db.session import db_helper

router = APIRouter(tags=["Products"])


@router.get("", response_model=list[ProductRetrieve])
async def get_products(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ]
):
    products = await list_products(session=session)
    return products


@router.get("/{product_id}", response_model=ProductRetrieve)
async def get_product(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    product_id: int
):
    product = await retrieve_product(session=session, product_id=product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


@router.post("", response_model=ProductRetrieve)
async def post_create_product(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    product: ProductCreate
) -> Product:
    product = await create_product(
        session=session,
        product_create=product
    )
    return product


@router.delete("/{product_id}")
async def delete_product(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    product_id: int
):
    product = await session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    await session.delete(product)
    await session.commit()
    return
