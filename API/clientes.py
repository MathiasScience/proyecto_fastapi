from fastapi import APIRouter, HTTPException, status
import asyncpg
from typing import List
from fastapi.params import Depends, Path, Query
from Conexion.coneccion import get_db_connection
from Esquemas.cliente import ClienteResponse
from core.api_key import validar_api_key

router = APIRouter(prefix="/clientes", tags=["clientes"],dependencies=[
        Depends(validar_api_key)
    ])

@router.get("/listar_productos", response_model=List[ClienteResponse])
async def listar_productos(
    conn: asyncpg.Connection = Depends(get_db_connection),
):
    rows = await conn.fetch("SELECT * FROM sp_obtener_clientes()")
    return [ClienteResponse(**dict(r)) for r in rows]
