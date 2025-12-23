from ntpath import join
from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base, get_db
from app.crud import crear_rol_inicial, crear_usuario_inicial, obtener_usuarios, obtener_roles, crear_rol, crear_usuario, update_rol, delete_rol, activate_rol, update_usuario, activate_usuario, delete_usuario
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
    return {"message": "API funcionando"}
@app.get("/usuarios", tags=["Usuarios"])
def listar_usuarios(db: Session = Depends(get_db)):
    usuarios = obtener_usuarios(db)
    roles = obtener_roles(db)
    # Crear un diccionario de roles para búsqueda rápida
    roles_dict = {r.id: r.rol_name for r in roles}
    
    return [
        {
            "id": u.id,
            "username": u.username,
            "rol": roles_dict.get(u.rol, "Sin rol"),
            "status": u.status,
            "created_at": u.created_at.isoformat(),
            "updated_at": u.updated_at.isoformat()
        }
        for u in usuarios
        if u.status == 1
    ]
@app.post("/crear_usuario", tags=["Usuarios"])
def endpoint_crear_usuario(
    db: Session = Depends(get_db),
    username: str = Query(...),
    password: str = Query(...),
    rol: int = Query(...)
):
    mensaje = crear_usuario(db, username=username, password=password, rol=rol)
    return {"mensaje": mensaje}
@app.put("/update_usuario", tags=["Usuarios"])
def endpoint_update_usuario(db: Session = Depends(get_db), old_username: str = Query(...), new_username: str = Query(...), new_rol: int = Query(...)):
    mensaje = update_usuario(db, old_username=old_username, new_username=new_username, new_rol=new_rol)
    return {"mensaje": mensaje}
@app.put("/delete_usuario", tags=["Usuarios"])
def endpoint_delete_usuario(db: Session = Depends(get_db), username: str = Query(...)):
    mensaje = delete_usuario(db, username=username)
    return {"mensaje": mensaje}
@app.put("/activate_usuario", tags=["Usuarios"])
def endpoint_activate_usuario(db: Session = Depends(get_db), username: str = Query(...)):
    mensaje = activate_usuario(db, username=username)
    return {"mensaje": mensaje}
@app.get("/roles", tags=["Roles"])
def listar_roles(db: Session = Depends(get_db)):
    roles = obtener_roles(db)
    return [
        {
            "id": r.id,
            "rol_name": r.rol_name,
            "status": r.status,
            "created_at": r.created_at.isoformat(),
            "updated_at": r.updated_at.isoformat()
        }
        for r in roles
        if r.status == 1
    ]
@app.post("/crear_rol", tags=["Roles"])
def endpoint_crear_rol(db: Session = Depends(get_db), rol_name: str = Query(...)):
    mensaje = crear_rol(db, rol_name)
    return {"mensaje": mensaje}
@app.put("/update_rol", tags=["Roles"])
def endpoint_update_rol(db: Session = Depends(get_db), old_rol_name: str = Query(...), new_rol_name: str = Query(...)):
    mensaje = update_rol(db, old_rol_name, new_rol_name)
    return {"mensaje": mensaje}
@app.put("/delete_rol", tags=["Roles"])
def endpoint_delete_rol(db: Session = Depends(get_db), rol_name: str = Query(...)):
    mensaje = delete_rol(db, rol_name)
    return {"mensaje": mensaje}
@app.put("/activate_rol", tags=["Roles"])
def endpoint_activate_rol(db: Session = Depends(get_db), rol_name: str = Query(...)):
    mensaje = activate_rol(db, rol_name)
    return {"mensaje": mensaje}