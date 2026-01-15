from fastapi import APIRouter, Depends, Body, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud.usuario import (
    create_usuario,
    get_usuario_by_username,
    update_usuario,
    delete_usuario,
    activate_usuario,
    login_usuario,
)
from app.models import Usuario, Rol

router = APIRouter()
users_router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@users_router.post("/")
def create_new_user(
    username: str = Body(...),
    password: str = Body(...),
    rol_id: int = Body(...),
    db: Session = Depends(get_db),
):
    existing_user = get_usuario_by_username(db, username=username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    try:
        usuario = create_usuario(
            db=db, username=username, password=password, rol_id=rol_id
        )
        return {
            "id": usuario.id,
            "username": usuario.username,
            "rol_id": usuario.rol_id,
            "status": usuario.status,
            "created_at": usuario.created_at,
            "updated_at": usuario.updated_at,
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@users_router.get("/")
def read_users(db: Session = Depends(get_db)):
    results = (
        db.query(
            Usuario.id,
            Usuario.username,
            Usuario.status,
            Usuario.created_at,
            Usuario.updated_at,
            Rol.nombre.label("rol_name"),
        )
        .join(Rol)
        .all()
    )

    return [
        {
            "id": r.id,
            "username": r.username,
            "rol_name": r.rol_name,
            "status": r.status,
            "created_at": r.created_at,
            "updated_at": r.updated_at,
        }
        for r in results
    ]


@users_router.put("/{user_id}")
def update_existing_user(
    user_id: int,
    username: str = Body(None),
    rol_id: int = Body(None),
    status: bool = Body(None),
    db: Session = Depends(get_db),
):
    try:
        updated_user = update_usuario(
            db=db, user_id=user_id, username=username, rol_id=rol_id, status=status
        )

        if not updated_user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        return {
            "id": updated_user.id,
            "username": updated_user.username,
            "rol_id": updated_user.rol_id,
            "status": updated_user.status,
            "created_at": updated_user.created_at,
            "updated_at": updated_user.updated_at,
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@users_router.delete("/{user_id}")
def delete_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    deleted_user = delete_usuario(db, user_id)
    if not deleted_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return {
        "message": "Usuario desactivado correctamente",
        "id": deleted_user.id,
        "status": deleted_user.status,
    }


@users_router.put("/{user_id}/activate")
def activate_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    activated_user = activate_usuario(db, user_id)
    if not activated_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return {
        "message": "Usuario activado correctamente",
        "id": activated_user.id,
        "status": activated_user.status,
    }


@router.post("/login", tags=["Usuarios"])
def login(
    username: str = Body(...), password: str = Body(...), db: Session = Depends(get_db)
):
    try:
        user_response = login_usuario(db, username, password)
        return {"message": "Login successful", "user": user_response}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


router.include_router(users_router)
