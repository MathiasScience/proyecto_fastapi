import asyncpg
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.security import OAuth2PasswordRequestForm
from Conexion.coneccion import get_db_connection
from Esquemas.usuario import LoginResponse, UsuarioBase, UsuarioCreate


router = APIRouter(prefix="/usuarios", tags=["usuarios"])


@router.get("/")
def leer_usuarios():
    return {"mensaje": "Lista de usuarios"}

@router.post("/", response_model=UsuarioBase, status_code=status.HTTP_201_CREATED)
async def crear_usuario(
    usuario_data: UsuarioCreate,
    conn: asyncpg.Connection = Depends(get_db_connection)
):
    print(usuario_data)
    row = await conn.fetchrow(
            "SELECT * FROM sp_crear_usuario($1, $2, $3)",
            usuario_data.nombre,
            usuario_data.email,
            usuario_data.password,
        )
    if not row:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se pudo verificar la creación de los usuarios")
    return UsuarioBase(**dict(row))

@router.post("/login")
async def validar_usuario(
    form_data: OAuth2PasswordRequestForm = Depends(),
    conn: asyncpg.Connection = Depends(get_db_connection)
):
    row = await conn.fetchrow(
            "SELECT * FROM sp_validar_usuario($1, $2)",
            form_data.username,
            form_data.password
        )
    if not row:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return "Usuario logeado"