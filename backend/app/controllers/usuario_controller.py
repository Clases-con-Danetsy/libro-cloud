from fastapi import APIRouter, Depends, Query, Path
from sqlalchemy.orm import Session, aliased
from app.database import get_db
from app.models import Usuario, Roles
from app.crud import (
    crear_usuario,
    obtener_usuarios,
    obtener_roles,
    update_usuario,
    delete_usuario,
    activate_usuario,
    verificar_credenciales,
    obtener_usuario_by_id,
)

router = APIRouter(prefix="/user", tags=["Usuarios"])


@router.get("/get")
def listar_usuarios(db: Session = Depends(get_db)):
    UserCreate = aliased(Usuario)
    UserUpdate = aliased(Usuario)

    data = (
        db.query(
            Usuario,
            UserCreate.username.label("created_by"),
            UserUpdate.username.label("updated_by"),
            Roles.rol_name.label("rol_name"),
        )
        .outerjoin(UserCreate, UserCreate.id == Usuario.who_create)
        .outerjoin(UserUpdate, UserUpdate.id == Usuario.who_update)
        .outerjoin(Roles, Roles.id == Usuario.rol)
        .all()
    )

    return [
        {
            "id": u.id,
            "username": u.username,
            "rol": rol_name,
            "status": u.status,
            "created_at": u.created_at.isoformat(),
            "updated_at": u.updated_at.isoformat(),
            "who_create": created_by,
            "who_update": updated_by,
        }
        for u, created_by, updated_by, rol_name in data
    ]


@router.get("/get/{id}")
def obtener_usuario_by_id_endpoint(
    id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
):
    usuario = obtener_usuario_by_id(db, id)
    return {
        "id": usuario.id,
        "username": usuario.username,
        "rol": usuario.rol,
        "status": usuario.status,
        "created_at": usuario.created_at.isoformat(),
        "updated_at": usuario.updated_at.isoformat(),
    }


@router.post("/create")
def crear_usuario_endpoint(
    db: Session = Depends(get_db),
    username: str = Query(...),
    password: str = Query(...),
    who_create: int = Query(...),
    who_update: int = Query(...),
    rol: int = Query(...),
):
    mensaje = crear_usuario(
        db,
        username=username,
        password=password,
        who_create=who_create,
        who_update=who_update,
        rol=rol,
    )
    return {"mensaje": mensaje}


@router.put("/update")
def actualizar_usuario(
    db: Session = Depends(get_db),
    id: int = Query(...),
    new_username: str = Query(...),
    new_rol: int = Query(...),
    who_update: int = Query(...),
):
    mensaje = update_usuario(
        db, id=id, new_username=new_username, new_rol=new_rol, who_update=who_update
    )
    return {"mensaje": mensaje}


@router.put("/activate")
def activar_usuario(db: Session = Depends(get_db), id: int = Query(...)):
    mensaje = activate_usuario(db, id=id)
    return {"mensaje": mensaje}


@router.delete("/delete")
def eliminar_usuario(db: Session = Depends(get_db), id: int = Query(...)):
    mensaje = delete_usuario(db, id=id)
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
        "user": {"username": usuario.username, "rol": rol_name, "id": usuario.id},
    }
