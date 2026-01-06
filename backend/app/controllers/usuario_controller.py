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
    role_id: int = Body(...),
    db: Session = Depends(get_db),
):
    existing_user = get_usuario_by_username(db, username=username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    try:
        return create_usuario(
            db=db, username=username, password=password, role_id=role_id
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@users_router.get("/")
def read_users(db: Session = Depends(get_db)):
    results = (
        db.query(
            Usuario.id, Usuario.username, Usuario.status, Rol.nombre.label("role_name")
        )
        .join(Rol)
        .all()
    )
    return [
        {
            "id": r.id,
            "username": r.username,
            "status": r.status,
            "role_name": r.role_name,
        }
        for r in results
    ]


@users_router.put("/{user_id}")
def update_existing_user(
    user_id: int,
    username: str = Body(None),
    role_id: int = Body(None),
    is_active: bool = Body(None),
    db: Session = Depends(get_db),
):
    try:
        updated_user = update_usuario(
            db=db,
            user_id=user_id,
            username=username,
            role_id=role_id,
            is_active=is_active,
        )
        if not updated_user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return {
            "id": updated_user.id,
            "username": updated_user.username,
            "role_id": updated_user.role_id,
            "is_active": updated_user.is_active,
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@users_router.delete("/{user_id}")
def delete_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    deleted_user = delete_usuario(db, user_id)
    if not deleted_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"message": "User deactivated successfully", "id": deleted_user.id}


@users_router.put("/{user_id}/activate")
def activate_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    activated_user = activate_usuario(db, user_id)
    if not activated_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"message": "User activated successfully", "id": activated_user.id}


@router.post("/login", tags=["Usuarios"])
def login(
    username: str = Body(...), password: str = Body(...), db: Session = Depends(get_db)
):
    try:
        user = login_usuario(db, username, password)
        return {
            "message": "Login successful",
            "user": {
                "id": user.id,
                "username": user.username,
                "rol_name": user.rol_name,
            },
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


router.include_router(users_router)
