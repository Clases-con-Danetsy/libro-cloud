from sqlalchemy.orm import Session
from app.models import Roles
from datetime import datetime


def crear_rol_inicial(db: Session):
    existe = db.query(Roles).filter(Roles.rol_name == "admin").first()
    if existe:
        return

    nuevo = Roles(
        rol_name="admin", status=1, created_at=datetime.now(), updated_at=datetime.now()
    )
    db.add(nuevo)
    db.commit()


def crear_rol(db: Session, rol_name: str):
    existe = db.query(Roles).filter(Roles.rol_name == rol_name).first()
    if existe:
        return

    nuevo = Roles(
        rol_name=rol_name,
        status=1,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    db.add(nuevo)
    db.commit()
    return "Rol creado correctamente"


def update_rol(db: Session, id: int, new_rol_name: str):
    rol = db.query(Roles).filter(Roles.id == id).first()
    if rol:
        rol.rol_name = new_rol_name
        rol.updated_at = datetime.now()
        db.add(rol)
        db.commit()
    return "Rol actualizado correctamente"


def delete_rol(db: Session, id: int):
    rol = db.query(Roles).filter(Roles.id == id).first()
    if rol:
        rol.status = 0
        rol.updated_at = datetime.now()
        db.add(rol)
        db.commit()
    return "Rol eliminado correctamente"


def activate_rol(db: Session, id: int):
    rol = db.query(Roles).filter(Roles.id == id).first()
    if rol:
        rol.status = 1
        rol.updated_at = datetime.now()
        db.add(rol)
        db.commit()
    return "Rol activado correctamente"


def obtener_roles(db: Session):
    return db.query(Roles).all()


def obtener_rol_by_id(db: Session, id: int):
    return db.query(Roles).filter(Roles.id == id).first()
