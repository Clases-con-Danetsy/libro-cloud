from fastapi import FastAPI
from app.database import Base, engine, SessionLocal
from app.crud.usuario import crear_usuario_inicial
from app.controllers import usuario_controller, rol_controller

app = FastAPI()

@app.on_event("startup")
def startup_event():
    print("🔧 Creando tablas si no existen...")
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    crear_usuario_inicial(db)
    db.close()

    print("✨ Usuario inicial creado (test / 123)")

@app.get("/")
def index():
    return {"status": "Backend Libro Cloud listo"}

app.include_router(usuario_controller.router)
app.include_router(rol_controller.router)
