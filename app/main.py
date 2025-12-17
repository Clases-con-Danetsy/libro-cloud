from ntpath import join
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base, get_db
from app.crud import crear_rol_inicial, crear_usuario_inicial, obtener_usuarios, obtener_roles

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

@app.get("/usuarios")
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
    ]

@app.get("/roles")
def listar_roles(db: Session = Depends(get_db)):
    roles = obtener_roles(db)
    # return [
    #     {
    #         "id": r.id,
    #         "rol_name": r.rol_name,
    #         "status": r.status,
    #         "created_at": r.created_at.isoformat(),
    #         "updated_at": r.updated_at.isoformat()
    #     }
    #     for r in roles
    # ]
    return roles
