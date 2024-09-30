from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Product
from core.schemas import ProductCreate, ProductRetrieve, ProductUpdate
from crud.products import (
    create_product,
    get_products,
    get_product,
    update_product
)
from db.session import db_helper

router = APIRouter(tags=["Products"])


@router.get("", response_model=list[ProductRetrieve])
async def get_list_products(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ]
):
    products = await get_products(session=session)
    return products


@router.get("/{product_id}", response_model=ProductRetrieve)
async def get_retrieve_product(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    product_id: int
):
    product = await get_product(session=session, product_id=product_id)

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


@router.put("/{product_id}", response_model=ProductRetrieve)
async def put_update_product(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    product_id: int,
    product: ProductUpdate
) -> Product:
    updated_product = await update_product(session=session, product_id=product_id, product=product)

    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")

    return updated_product


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
