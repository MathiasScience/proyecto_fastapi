from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

# 1. Modelo para CREAR un cliente (Datos que envía el cliente por POST)
class ClienteCreate(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100, description="Nombre completo del cliente")
    email: EmailStr = Field(..., description="Correo electrónico válido")
    telefono: str | None = Field(default=None, max_length=20, description="Teléfono de contacto opcional")

# 2. Modelo para OBTENER/DEVOLVER un cliente (Datos que la API responde al usuario)
class ClienteResponse(BaseModel):
    id: int
    nombre: str
    email: str
    telefono: str | None = None
    activo: bool
    creado_en: datetime

    class Config:
        from_attributes = True  # Permite mapear modelos directamente desde objetos uORM / tuplas de base de datos