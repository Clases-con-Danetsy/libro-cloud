from fastapi import APIRouter, Depends, Body, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud.rol import get_roles, create_role, get_role_by_name, delete_role, activate_role, update_role

router = APIRouter(prefix="/roles", tags=["Roles"])

@router.post("/")
def create_new_role(role_name: str = Body(..., embed=True), db: Session = Depends(get_db)):
    db_role = get_role_by_name(db, nombre=role_name)
    if db_role:
        raise HTTPException(status_code=400, detail="Role already exists")
    return create_role(db=db, nombre=role_name)

@router.get("/")
def read_roles(db: Session = Depends(get_db)):
    return get_roles(db)

@router.delete("/{role_id}")
def delete_role_endpoint(role_id: int, db: Session = Depends(get_db)):
    deleted_role = delete_role(db, role_id)
    if not deleted_role:
        raise HTTPException(status_code=404, detail="Role not found")
    return {"message": "Role deactivated successfully", "id": deleted_role.id}

@router.put("/{role_id}/activate")
def activate_role_endpoint(role_id: int, db: Session = Depends(get_db)):
    activated_role = activate_role(db, role_id)
    if not activated_role:
        raise HTTPException(status_code=404, detail="Role not found")
    return {"message": "Role activated successfully", "id": activated_role.id}

@router.put("/{role_id}")
def update_existing_role(
    role_id: int,
    role_name: str = Body(None, embed=True),
    is_active: bool = Body(None, embed=True),
    db: Session = Depends(get_db)
):
    updated_role = update_role(db=db, role_id=role_id, nombre=role_name, is_active=is_active)
    if not updated_role:
        raise HTTPException(status_code=404, detail="Role not found")
    return updated_role
