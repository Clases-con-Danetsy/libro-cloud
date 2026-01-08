from fastapi import APIRouter, Depends, Body, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud.rol import get_roles, create_role, get_role_by_name, delete_role, activate_role, update_role

router = APIRouter(prefix="/roles", tags=["Roles"])

@router.post("/")
def create_new_role(nombre: str = Body(..., embed=True), db: Session = Depends(get_db)):
    db_role = get_role_by_name(db, nombre=nombre)
    if db_role:
        raise HTTPException(status_code=400, detail="Role already exists")
    return create_role(db=db, nombre=nombre)

@router.get("/")
def read_roles(db: Session = Depends(get_db)):
    return get_roles(db)

@router.delete("/{rol_id}")
def delete_role_endpoint(rol_id: int, db: Session = Depends(get_db)):
    deleted_role = delete_role(db, rol_id)
    if not deleted_role:
        raise HTTPException(status_code=404, detail="Role not found")
    return {"message": "Role deactivated successfully", "id": deleted_role.id}

@router.put("/{rol_id}/activate")
def activate_role_endpoint(rol_id: int, db: Session = Depends(get_db)):
    activated_role = activate_role(db, rol_id)
    if not activated_role:
        raise HTTPException(status_code=404, detail="Role not found")
    return {"message": "Role activated successfully", "id": activated_role.id}

@router.put("/{rol_id}")
def update_existing_role(
    rol_id: int,
    nombre: str = Body(None, embed=True),
    is_active: bool = Body(None, embed=True),
    db: Session = Depends(get_db)
):
    updated_role = update_role(db=db, rol_id=rol_id, nombre=nombre, is_active=is_active)
    if not updated_role:
        raise HTTPException(status_code=404, detail="Role not found")
    return updated_role
