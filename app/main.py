from fastapi import FastAPI, Depends, Body, HTTPException
from sqlalchemy.orm import Session
from app.database import Base, engine, SessionLocal, get_db
from app.crud.usuario import crear_usuario_inicial, create_usuario, get_usuario_by_username, update_usuario, delete_usuario, activate_usuario
from app.models import Usuario, Rol   # importa modelos explícitamente o todos con *
from app.crud.rol import get_roles, create_role, get_role_by_name, delete_role, activate_role, update_role

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
    existing_user = get_usuario_by_username(db, username=username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
        
    try:
        return create_usuario(db=db, username=username, password=password, role_id=role_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

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

@app.put("/usuarios/{user_id}")
def update_existing_user(
    user_id: int,
    username: str = Body(None),
    role_id: int = Body(None),
    is_active: bool = Body(None),
    db: Session = Depends(get_db)
):
    try:
        updated_user = update_usuario(db=db, user_id=user_id, username=username, role_id=role_id, is_active=is_active)
        if not updated_user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return {
            "id": updated_user.id,
            "username": updated_user.username,
            "role_id": updated_user.role_id,
            "is_active": updated_user.is_active
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/roles/{role_id}")
def delete_role_endpoint(role_id: int, db: Session = Depends(get_db)):
    deleted_role = delete_role(db, role_id)
    if not deleted_role:
        raise HTTPException(status_code=404, detail="Role not found")
    return {"message": "Role deactivated successfully", "id": deleted_role.id}

@app.delete("/usuarios/{user_id}")
def delete_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    deleted_user = delete_usuario(db, user_id)
    if not deleted_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"message": "User deactivated successfully", "id": deleted_user.id}

@app.put("/roles/{role_id}/activate")
def activate_role_endpoint(role_id: int, db: Session = Depends(get_db)):
    activated_role = activate_role(db, role_id)
    if not activated_role:
        raise HTTPException(status_code=404, detail="Role not found")
    return {"message": "Role activated successfully", "id": activated_role.id}

@app.put("/roles/{role_id}")
def update_existing_role(
    role_id: int,
    role_name: str = Body(None, embed=True),
    is_active: bool = Body(None, embed=True),
    db: Session = Depends(get_db)
):
    updated_role = update_role(db=db, role_id=role_id, nombre=role_name, is_active=is_active)
    if not updated_role:
        raise HTTPException(status_code=404, detail="Role not found")
    return updated_role

@app.put("/usuarios/{user_id}/activate")
def activate_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    activated_user = activate_usuario(db, user_id)
    if not activated_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"message": "User activated successfully", "id": activated_user.id}
