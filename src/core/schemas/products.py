from typing import Optional

from pydantic import BaseModel, condecimal


class ProductBase(BaseModel):
    name: str
    description: str
    price: condecimal(decimal_places=2)
    quantity: int


class ProductCreate(ProductBase):
    pass


class ProductRetrieve(ProductBase):
    id: int


class ProductUpdate(ProductBase):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[condecimal(decimal_places=2)] = None
    quantity: Optional[int] = None
