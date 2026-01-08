from sqlalchemy.orm import Session
from app.models.rol import Rol


def get_roles(db: Session):
    return db.query(Rol).all()

def get_role_by_name(db: Session, nombre: str):
    return db.query(Rol).filter(Rol.nombre == nombre).first()

def create_role(db: Session, nombre: str):
    db_role = Rol(nombre=nombre)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

def delete_role(db: Session, rol_id: int):
    db_role = db.query(Rol).filter(Rol.id == rol_id).first()
    if not db_role:
        return None
    db_role.is_active = False
    db.commit()
    db.refresh(db_role)
    return db_role

def activate_role(db: Session, rol_id: int):
    db_role = db.query(Rol).filter(Rol.id == rol_id).first()
    if not db_role:
        return None
    db_role.is_active = True
    db.commit()
    db.refresh(db_role)
    return db_role

def update_role(db: Session, rol_id: int, nombre: str = None, is_active: bool = None):
    db_role = db.query(Rol).filter(Rol.id == rol_id).first()
    if not db_role:
        return None
    
    if nombre is not None:
        db_role.nombre = nombre
    
    if is_active is not None:
        db_role.is_active = is_active
        
    db.commit()
    db.refresh(db_role)
    return db_role
