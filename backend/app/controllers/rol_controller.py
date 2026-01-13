from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud import crear_rol, obtener_roles, update_rol, delete_rol, activate_rol

router = APIRouter(prefix="/rol", tags=["Roles"])


@router.get("/get")
def listar_roles(db: Session = Depends(get_db)):
    roles = obtener_roles(db)
    return [
        {
            "id": r.id,
            "rol_name": r.rol_name,
            "status": r.status,
            "created_at": r.created_at.isoformat(),
            "updated_at": r.updated_at.isoformat(),
        }
        for r in roles
    ]


@router.post("/create")
def crear_rol_endpoint(db: Session = Depends(get_db), rol_name: str = Query(...)):
    mensaje = crear_rol(db, rol_name)
    return {"mensaje": mensaje}


@router.put("/update")
def actualizar_rol(
    db: Session = Depends(get_db),
    old_rol_name: str = Query(...),
    new_rol_name: str = Query(...),
):
    mensaje = update_rol(db, old_rol_name, new_rol_name)
    return {"mensaje": mensaje}


@router.put("/activate")
def activar_rol(db: Session = Depends(get_db), id: int = Query(...)):
    mensaje = activate_rol(db, id)
    return {"mensaje": mensaje}


@router.delete("/delete")
def eliminar_rol(db: Session = Depends(get_db), id: int = Query(...)):
    mensaje = delete_rol(db, id)
    return {"mensaje": mensaje}
