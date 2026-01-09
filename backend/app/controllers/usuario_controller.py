from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud import (
    crear_usuario,
    obtener_usuarios,
    obtener_roles,
    update_usuario,
    delete_usuario,
    activate_usuario,
    verificar_credenciales,
)

router = APIRouter(prefix="/user", tags=["Usuarios"])


@router.get("/get")
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
            "updated_at": u.updated_at.isoformat(),
        }
        for u in usuarios
    ]


@router.post("/create")
def crear_usuario_endpoint(
    db: Session = Depends(get_db),
    username: str = Query(...),
    password: str = Query(...),
    rol: int = Query(...),
):
    mensaje = crear_usuario(db, username=username, password=password, rol=rol)
    return {"mensaje": mensaje}


@router.put("/update")
def actualizar_usuario(
    db: Session = Depends(get_db),
    old_username: str = Query(...),
    new_username: str = Query(...),
    new_rol: int = Query(...),
):
    mensaje = update_usuario(
        db, old_username=old_username, new_username=new_username, new_rol=new_rol
    )
    return {"mensaje": mensaje}


@router.put("/activate")
def activar_usuario(db: Session = Depends(get_db), username: str = Query(...)):
    mensaje = activate_usuario(db, username=username)
    return {"mensaje": mensaje}


@router.delete("/delete")
def eliminar_usuario(db: Session = Depends(get_db), username: str = Query(...)):
    mensaje = delete_usuario(db, username=username)
    return {"mensaje": mensaje}


@router.post("/login")
def login(
    db: Session = Depends(get_db),
    username: str = Query(..., description="Nombre de usuario"),
    password: str = Query(..., description="Contraseña"),
):

    usuario, error = verificar_credenciales(db, username, password)

    if error:
        return {"success": False, "message": error}
    roles = obtener_roles(db)
    roles_dict = {r.id: r.rol_name for r in roles}
    rol_name = roles_dict.get(usuario.rol)

    return {
        "success": True,
        "message": "Login exitoso",
        "user": {"username": usuario.username, "rol": rol_name},
    }
