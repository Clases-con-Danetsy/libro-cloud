from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine, SessionLocal
from app.repository.usuario import crear_usuario_inicial
from app.controllers import usuario_controller, rol_controller

app = FastAPI()

origins = [
    "http://localhost:4321",
    "http://127.0.0.1:4321",  # ✅ Agregar esta línea
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
