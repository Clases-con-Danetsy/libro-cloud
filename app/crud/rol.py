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
