from sqlalchemy.orm import Session
from app.models.rol import Rol


def get_roles(db: Session):
    return db.query(Rol).all()


def get_role_by_name(db: Session, nombre: str):
    return db.query(Rol).filter(Rol.nombre == nombre).first()


def get_role_by_id(db: Session, id: int):
    return db.query(Rol).filter(Rol.id == id).first()


def create_role(db: Session, nombre: str, created_by: int, updated_by: int):
    db_role = Rol(nombre=nombre, status=True, created_by=created_by, updated_by=updated_by)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role


def delete_role(db: Session, rol_id: int, id_user: int):
    db_role = db.query(Rol).filter(Rol.id == rol_id).first()
    if not db_role:
        return None
    db_role.status = False
    db_role.updated_by = id_user  # ✅ Registrar quién desactivó
    db.commit()
    db.refresh(db_role)
    return db_role


def activate_role(db: Session, rol_id: int, id_user: int):
    db_role = db.query(Rol).filter(Rol.id == rol_id).first()
    if not db_role:
        return None
    db_role.status = True
    db_role.updated_by = id_user  # ✅ Registrar quién activó
    db.commit()
    db.refresh(db_role)
    return db_role

def update_role(db: Session, rol_id: int, nombre: str = None, status: bool = None, updated_by: int = None):
    db_role = db.query(Rol).filter(Rol.id == rol_id).first()
    if not db_role:
        return None

    if nombre is not None:
        db_role.nombre = nombre

    if status is not None:
        db_role.status = status

    if updated_by is not None:
        db_role.updated_by = updated_by

    db.commit()
    db.refresh(db_role)
    return db_role
