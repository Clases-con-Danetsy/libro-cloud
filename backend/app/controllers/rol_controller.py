from fastapi import APIRouter, Depends, Body, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.deps import get_current_user
from app.repository.usuario import get_users_by_ids
from app.repository.rol import (
    get_roles,
    create_role,
    get_role_by_name,
    delete_role,
    activate_role,
    update_role,
    get_role_by_id,
)

router = APIRouter(prefix="/roles", tags=["Roles"])


@router.post("/")
def create_new_role(
    nombre: str = Body(..., embed=True),
    user_id: int = Body(..., embed=True),
    current_user: int = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    db_role = get_role_by_name(db, nombre=nombre)
    if db_role:
        raise HTTPException(status_code=400, detail="Role already exists")

    role = create_role(db=db, nombre=nombre, created_by=user_id, updated_by=user_id)

    return {
        "id": role.id,
        "nombre": role.nombre,
        "status": role.status,
        "created_at": role.created_at,
        "updated_at": role.updated_at,
        "created_by": role.created_by,
        "updated_by": role.updated_by,
    }


@router.get("/")
def read_roles(
    current_user: int = Depends(get_current_user), db: Session = Depends(get_db)
):
    roles = get_roles(db)

    user_ids = set()
    for r in roles:
        if r.created_by:
            user_ids.add(r.created_by)
        if r.updated_by:
            user_ids.add(r.updated_by)

    users = get_users_by_ids(db, list(user_ids))
    user_map = {u.id: u.username for u in users}

    return [
        {
            "id": r.id,
            "nombre": r.nombre,
            "status": r.status,
            "created_at": r.created_at,
            "updated_at": r.updated_at,
            "created_by": user_map.get(r.created_by),
            "updated_by": user_map.get(r.updated_by),
        }
        for r in roles
    ]


@router.get("/{rol_id}")
def read_role_by_id(
    rol_id: int,
    current_user: int = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    role = get_role_by_id(db, rol_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return {
        "id": role.id,
        "nombre": role.nombre,
        "status": role.status,
        "created_at": role.created_at,
        "updated_at": role.updated_at,
    }


@router.delete("/{rol_id}")
def delete_role_endpoint(
    rol_id: int,
    current_user: int = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    deleted_role = delete_role(db, rol_id, current_user)
    if not deleted_role:
        raise HTTPException(status_code=404, detail="Role not found")

    return {
        "message": "Role deactivated successfully",
        "id": deleted_role.id,
        "status": deleted_role.status,
    }


@router.put("/{rol_id}/activate")
def activate_role_endpoint(
    rol_id: int,
    current_user: int = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    activated_role = activate_role(db, rol_id, current_user)
    if not activated_role:
        raise HTTPException(status_code=404, detail="Role not found")

    return {
        "message": "Role activated successfully",
        "id": activated_role.id,
        "status": activated_role.status,
    }


@router.put("/{rol_id}")
def update_existing_role(
    rol_id: int,
    nombre: str = Body(None, embed=True),
    status: bool = Body(None, embed=True),
    user_id: int = Body(..., embed=True),
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):

    updated_role = update_role(
        db=db, rol_id=rol_id, nombre=nombre, status=status, updated_by=user_id
    )

    if not updated_role:
        raise HTTPException(status_code=404, detail="Role not found")

    return {
        "id": updated_role.id,
        "nombre": updated_role.nombre,
        "status": updated_role.status,
        "created_at": updated_role.created_at,
        "updated_at": updated_role.updated_at,
        "updated_by": updated_role.updated_by,
        "created_by": updated_role.created_by,
    }
