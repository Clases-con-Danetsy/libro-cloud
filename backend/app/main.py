from fastapi import FastAPI
from app.database import SessionLocal, engine, Base
from app.crud import crear_rol_inicial, crear_usuario_inicial
from app.controllers import usuario_router, rol_router

app = FastAPI(title="Libro Cloud API")

print("🔧 Creando tablas si no existen...")
Base.metadata.create_all(bind=engine)

@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    try:
        crear_rol_inicial(db)
        crear_usuario_inicial(db)
        print("✨ Inicialización completada")
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Libro Cloud API Funcionando Correctamente"}

# Incluir routers de los controladores
app.include_router(usuario_router)
app.include_router(rol_router)