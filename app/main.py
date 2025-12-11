from fastapi import FastAPI
from app.database import Base, engine, SessionLocal
from app.crud import crear_usuario_inicial
from app.models import *   # importa todos los modelos

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
