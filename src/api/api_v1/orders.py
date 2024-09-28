from typing import Annotated, Sequence

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Order
from core.schemas import OrderResponse, OrderCreate, OrderStatus
from crud.orders import (
    list_orders, create_order, retrieve_order, updated_order_status,
)

from db.session import db_helper

router = APIRouter(tags=["Orders"])


@router.get("", response_model=list[OrderResponse])
async def get_list_orders(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ]
) -> Sequence[Order]:
    orders = await list_orders(session=session)
    return orders


@router.get("/{order_id}", response_model=OrderResponse)
async def get_retrieve_order(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    order_id: int
) -> Order:
    order = await retrieve_order(session=session, order_id=order_id)
    return order


@router.post("", response_model=OrderResponse)
async def post_create_order(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    order_create: OrderCreate,
) -> Order:
    order = await create_order(session=session, order_create=order_create)

    session.add(order)
    await session.commit()
    await session.refresh(order)
    return order


@router.patch("/{order_id}/status", response_model=OrderResponse)
async def patch_order_status(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    order_id: int,
    status: OrderStatus
):
    updated_order = await updated_order_status(session=session, order_id=order_id, status=status)
    if not updated_order:
        raise HTTPException(status_code=404, detail="Order not found")

    await session.commit()
    await session.refresh(updated_order)
    return updated_order
