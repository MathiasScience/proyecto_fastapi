"""
Manejo del pool de conexiones asyncpg y generador de conexión por request.
- Inicializa un pool global en el ciclo de vida de la app (startup/shutdown) o usando lifespan.
- Provee la dependencia `get_db_connection` para inyectar conexiones en endpoints con FastAPI Depends.
"""
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Optional

import asyncpg

from core.config import get_settings

_pool: Optional[asyncpg.Pool] = None


async def init_db_pool() -> asyncpg.Pool:
    """Inicializa y devuelve el pool global si no existe."""
    global _pool
    if _pool is None:
        settings = get_settings()
        _pool = await asyncpg.create_pool(
            dsn=settings.database_dsn,
            min_size=settings.db_min_connections,
            max_size=settings.db_max_connections,
        )
    return _pool


async def close_db_pool() -> None:
    """Cierra el pool global si existe."""
    global _pool
    if _pool is not None:
        await _pool.close()
        _pool = None


@asynccontextmanager
async def lifespan_db():
    """Contexto para usar en FastAPI lifespan: asegura pool disponible y lo cierra al final."""
    await init_db_pool()
    try:
        yield
    finally:
        await close_db_pool()


async def get_db_connection() -> AsyncGenerator[asyncpg.Connection, None]:
    """
    Generador de conexión de base de datos para usar con Depends.
    Obtiene una conexión del pool y la cede al contexto del endpoint.
    """
    pool = await init_db_pool()
    async with pool.acquire() as conn:
        # Asegurar configuración consistente por conexión si fuese necesario
        # await conn.set_type_codec('json', encoder=json.dumps, decoder=json.loads, schema='pg_catalog')
        yield conn