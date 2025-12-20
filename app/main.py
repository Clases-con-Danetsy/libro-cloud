from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.database import Base, engine, SessionLocal, get_db
from app.crud import crear_usuario_inicial
from app.models import Usuario, Rol   # importa modelos explícitamente o todos con *

app = FastAPI()

@app.on_event("startup")
def startup_event():
    print("🔧 Creando tablas si no existen...")
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    # Verificar existencia de rol admin
    rol_admin = db.query(Rol).filter(Rol.nombre == "admin").first()
    if not rol_admin:
        print("🔧 Creando rol 'admin'...")
        nuevo_rol = Rol(nombre="admin")
        db.add(nuevo_rol)
        db.commit()

    crear_usuario_inicial(db)
    db.close()

    print("✨ Usuario inicial creado (test / 123)")

@app.get("/")
def index():
    return {"status": "Backend Libro Cloud listo"}

@app.get("/roles")
def read_roles(db: Session = Depends(get_db)):
    return db.query(Rol).all()

@app.get("/usuarios")
def read_users(db: Session = Depends(get_db)):
    results = db.query(Usuario.id, Usuario.username, Usuario.status, Rol.nombre.label("role_name")).join(Rol).all()
    return [
        {
            "id": r.id,
            "username": r.username,
            "status": r.status,
            "role_name": r.role_name
        }
        for r in results
    ]   
