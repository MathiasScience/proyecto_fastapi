from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, condecimal, NonNegativeInt


DecimalMoneda = condecimal(max_digits=14, decimal_places=2, ge=0)


class ProductoBase(BaseModel):
    nombre: str = Field(min_length=1, max_length=255)
    precio: DecimalMoneda
    stock: NonNegativeInt


class ProductoCreate(ProductoBase):
    pass


class ProductoUpdate(BaseModel):
    nombre: Optional[str] = Field(default=None, min_length=1, max_length=255)
    precio: Optional[DecimalMoneda] = None
    stock: Optional[NonNegativeInt] = None


class ProductoOut(ProductoBase):
    id: int
    creado_en: datetime
    actualizado_en: datetime