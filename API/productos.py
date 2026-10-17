from typing import List

import asyncpg
from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends, Path, Query

from Conexion.coneccion import get_db_connection
from Esquemas.producto import ProductoOut

router = APIRouter(prefix="/productos", tags=["productos"])


@router.get("/", response_model=List[ProductoOut])
async def listar_productos(
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=1000),
    conn: asyncpg.Connection = Depends(get_db_connection),
):
    rows = await conn.fetch("SELECT * FROM sp_listar_productos($1, $2)", offset, limit)
    return [ProductoOut(**dict(r)) for r in rows]


@router.get("/{id}", response_model=ProductoOut)
async def obtener_producto(
    id: int = Path(..., ge=1),
    conn: asyncpg.Connection = Depends(get_db_connection)
):
    row = await conn.fetchrow("SELECT * FROM sp_obtener_producto_por_id($1)", id)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    return ProductoOut(**dict(row))


@router.post("/", response_model=ProductoOut, status_code=status.HTTP_201_CREATED)
async def crear_producto(
    nombre: str = Query(..., min_length=2, max_length=20),
    precio: float = Query(..., gt=0, le=5734000000000),
    stock: int = Query(..., ge=0, le=10000),
    conn: asyncpg.Connection = Depends(get_db_connection)
):
    await conn.execute("SELECT sp_crear_producto($1, $2, $3)", nombre, precio, stock)
    row = await conn.fetchrow("SELECT * FROM productos WHERE nombre = $1 ORDER BY id DESC LIMIT 1", nombre)
    if not row:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se pudo verificar la creación del producto")
    return ProductoOut(**dict(row))


@router.put("/{id}", response_model=ProductoOut)
async def actualizar_producto(
    id: int = Path(..., ge=1),
    nombre: str = Query(..., min_length=2, max_length=20),
    precio: float = Query(..., gt=0, le=5734000000000),
    stock: int = Query(..., ge=0, le=10000),
    conn: asyncpg.Connection = Depends(get_db_connection)
):
    row = await conn.fetchrow("SELECT (sp_actualizar_producto($1, $2, $3, $4)).*", id, nombre, precio, stock)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado para actualizar")
    return ProductoOut(**dict(row))


@router.delete("/{producto_id}")
async def eliminar_producto(
    producto_id: int = Path(..., ge=1),
    conn: asyncpg.Connection = Depends(get_db_connection)
):
    existe = await conn.fetchval("SELECT EXISTS(SELECT 1 FROM productos WHERE id = $1)", producto_id)
    if not existe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    await conn.execute("SELECT sp_eliminar_producto($1)", producto_id)
    return None
