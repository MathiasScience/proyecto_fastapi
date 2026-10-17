from fastapi import FastAPI
from API.productos import router as productos_router
from API.usuarios import router as usuarios_router
from API.clientes import router as clientes_router

app = FastAPI()

# Incluir cada router explícitamente
app.include_router(productos_router)
app.include_router(usuarios_router)
app.include_router(clientes_router)


@app.get("/")
def root():
    return {"mensaje": "API funcionando correctamente"}
