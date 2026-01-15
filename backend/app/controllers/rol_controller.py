from fastapi import APIRouter, Depends, Body, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud.rol import (
    get_roles,
    create_role,
    get_role_by_name,
    delete_role,
    activate_role,
    update_role,
)

router = APIRouter(prefix="/roles", tags=["Roles"])


@router.post("/")
def create_new_role(nombre: str = Body(..., embed=True), db: Session = Depends(get_db)):
    db_role = get_role_by_name(db, nombre=nombre)
    if db_role:
        raise HTTPException(status_code=400, detail="Role already exists")

    role = create_role(db=db, nombre=nombre)

    return {
        "id": role.id,
        "nombre": role.nombre,
        "status": role.status,
        "created_at": role.created_at,
        "updated_at": role.updated_at,
    }


@router.get("/")
def read_roles(db: Session = Depends(get_db)):
    roles = get_roles(db)
    return [
        {
            "id": r.id,
            "nombre": r.nombre,
            "status": r.status,
            "created_at": r.created_at,
            "updated_at": r.updated_at,
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
        "status": deleted_role.status,
    }


@router.put("/{rol_id}/activate")
def activate_role_endpoint(rol_id: int, db: Session = Depends(get_db)):
    activated_role = activate_role(db, rol_id)
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
    db: Session = Depends(get_db),
):
    updated_role = update_role(db=db, rol_id=rol_id, nombre=nombre, status=status)

    if not updated_role:
        raise HTTPException(status_code=404, detail="Role not found")

    return {
        "id": updated_role.id,
        "nombre": updated_role.nombre,
        "status": updated_role.status,
        "created_at": updated_role.created_at,
        "updated_at": updated_role.updated_at,
    }
