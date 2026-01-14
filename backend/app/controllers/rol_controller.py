from fastapi import APIRouter, Depends, Body, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud.rol import (
    get_roles,
    create_role,
    get_role_by_name,
    delete_role,
    activate_role,
    update_role
)

router = APIRouter(prefix="/roles", tags=["Roles"])


@router.post("/")
def create_new_role(
    nombre: str = Body(..., embed=True),
    db: Session = Depends(get_db)
):
    db_role = get_role_by_name(db, nombre=nombre)
    if db_role:
        raise HTTPException(status_code=400, detail="Role already exists")

    role = create_role(db=db, nombre=nombre)

    return {
        "id": role.id,
        "nombre": role.nombre,
        "is_active": role.is_active,
        "created_at": role.created_at,
        "updated_at": role.updated_at
    }


@router.get("/")
def read_roles(db: Session = Depends(get_db)):
    roles = get_roles(db)
    return [
        {
            "id": r.id,
            "nombre": r.nombre,
            "is_active": r.is_active,
            "created_at": r.created_at,
            "updated_at": r.updated_at
        }
        for r in roles
    ]


@router.delete("/{rol_id}")
def delete_role_endpoint(rol_id: int, db: Session = Depends(get_db)):
    deleted_role = delete_role(db, rol_id)
    if not deleted_role:
        raise HTTPException(status_code=404, detail="Role not found")

    return {
        "message": "Role deactivated successfully",
        "id": deleted_role.id,
        "is_active": deleted_role.is_active
    }


@router.put("/{rol_id}/activate")
def activate_role_endpoint(rol_id: int, db: Session = Depends(get_db)):
    activated_role = activate_role(db, rol_id)
    if not activated_role:
        raise HTTPException(status_code=404, detail="Role not found")

    return {
        "message": "Role activated successfully",
        "id": activated_role.id,
        "is_active": activated_role.is_active
    }


@router.put("/{rol_id}")
def update_existing_role(
    rol_id: int,
    nombre: str = Body(None, embed=True),
    is_active: int = Body(None, embed=True),
    db: Session = Depends(get_db)
):
    updated_role = update_role(
        db=db,
        rol_id=rol_id,
        nombre=nombre,
        is_active=is_active
    )

    if not updated_role:
        raise HTTPException(status_code=404, detail="Role not found")

    return {
        "id": updated_role.id,
        "nombre": updated_role.nombre,
        "is_active": updated_role.is_active,
        "created_at": updated_role.created_at,
        "updated_at": updated_role.updated_at
    }
