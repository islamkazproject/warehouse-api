from typing import Annotated, Sequence

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Order
from core.schemas import OrderCreate, OrderResponse, OrderStatus
from crud.orders import (
    create_order,
    get_orders,
    get_order,
    update_order_status
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
    orders = await get_orders(session=session)
    return orders


@router.get("/{order_id}", response_model=OrderResponse)
async def get_retrieve_order(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    order_id: int
) -> Order:
    order = await get_order(session=session, order_id=order_id)
    return order


@router.post("", response_model=OrderResponse)
async def post_create_order(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    order_create: OrderCreate,
) -> Order:
    try:
        order = await create_order(session=session, order_create=order_create)
        session.add(order)
        await session.commit()
        await session.refresh(order)
        return order
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{order_id}/status", response_model=OrderResponse)
async def patch_order_status(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    order_id: int,
    status: OrderStatus
) -> Order:
    try:
        updated_order = await update_order_status(session=session, order_id=order_id, status=status)

        if not updated_order:
            raise HTTPException(status_code=404, detail="Order not found")

        await session.refresh(updated_order)
        return updated_order
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
