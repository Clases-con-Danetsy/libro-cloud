from fastapi import FastAPI, Depends, Body, HTTPException
from sqlalchemy.orm import Session
from app.database import Base, engine, SessionLocal, get_db
from app.crud.usuario import crear_usuario_inicial, create_usuario, get_usuario_by_username
from app.models import Usuario, Rol   # importa modelos explícitamente o todos con *
from app.crud.rol import get_roles, create_role, get_role_by_name

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

@app.post("/roles")
def create_new_role(role_name: str = Body(..., embed=True), db: Session = Depends(get_db)):
    db_role = get_role_by_name(db, nombre=role_name)
    if db_role:
        raise HTTPException(status_code=400, detail="Role already exists")
    return create_role(db=db, nombre=role_name)

@app.get("/roles")
def read_roles(db: Session = Depends(get_db)):
    return get_roles(db)

@app.post("/usuarios")
def create_new_user(
    username: str = Body(...),
    password: str = Body(...),
    role_id: int = Body(...),
    db: Session = Depends(get_db)
):
    role = db.query(Rol).filter(Rol.id == role_id).first()
    if not role:
        raise HTTPException(status_code=400, detail="Role not found")
        
    existing_user = get_usuario_by_username(db, username=username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
        
    return create_usuario(db=db, username=username, password=password, role_id=role_id)

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
