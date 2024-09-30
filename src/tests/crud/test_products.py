from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from core.schemas import ProductCreate, ProductUpdate
from crud.products import create_product, get_product, update_product, get_products


async def test_create_product(db_session: AsyncSession):
    product_data = ProductCreate(
        name="Test Product",
        description="Test Description",
        quantity=20,
        price=Decimal(10.99)
    )
    product = await create_product(db_session, product_data)

    assert product.id is not None
    assert product.name == "Test Product"
    assert product.price == 10.99


async def test_get_product(db_session: AsyncSession):
    product_data = ProductCreate(
        name="Test Product",
        description="Test Description",
        quantity=20,
        price=Decimal(10)
    )
    created_product = await create_product(db_session, product_data)

    product = await get_product(db_session, created_product.id)

    await db_session.commit()

    assert product is not None
    assert product.id == created_product.id
    assert product.name == "Test Product"
    assert product.price == 10.99


async def test_get_products(db_session: AsyncSession):
    product_data_1 = ProductCreate(
        name="Test Product",
        description="Test Description",
        quantity=20,
        price=Decimal(10)
    )
    product_data_2 = ProductCreate(
        name="Test Product 2",
        description="Test Description 2",
        quantity=100,
        price=Decimal(1000)
    )

    await create_product(db_session, product_data_1)
    await create_product(db_session, product_data_2)

    products = await get_products(db_session)

    await db_session.commit()

    assert len(products) == 2
    assert products[0].name == "Test Product"
    assert products[1].name == "Test Product 2"


async def test_update_product(db_session: AsyncSession):
    product_data = ProductCreate(
        name="Old product",
        description="Test Description 2",
        quantity=100,
        price=Decimal(1000)
    )
    created_product = await create_product(db_session, product_data)

    update_data = ProductUpdate(
        name="Updated Product",
        description="Test Description 2",
        quantity=100,
        price=Decimal(7.99)
    )
    updated_product = await update_product(db_session, created_product.id, update_data)

    await db_session.commit()

    assert updated_product.name == "Updated Product"
    assert updated_product.price == 7.99
