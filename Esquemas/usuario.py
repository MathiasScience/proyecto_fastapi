"""
Esquemas Pydantic v2 para Usuario y Token.
"""
from typing import Optional

from pydantic import BaseModel, EmailStr


class UsuarioBase(BaseModel):
    id: int
    nombre: str
    email: EmailStr
    activo: bool


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int  # segundos


class LoginResponse(BaseModel):
    user: UsuarioBase
    token: Token


class OAuth2PasswordRequestFormPatched(BaseModel):
    """
    Útil para pruebas manuales fuera de Swagger; normalmente usar `OAuth2PasswordRequestForm` de FastAPI
    en el endpoint. Aquí lo dejamos por si se desea usar como body JSON.
    """
    username: EmailStr
    password: str
    scope: Optional[str] = ""


# --- Esquemas de Pydantic ---
class UsuarioCreate(BaseModel):
    nombre: str
    email: EmailStr
    password: str