from sqlalchemy.orm import Session
from app.models import Roles
from datetime import datetime

def crear_rol_inicial(db: Session):
    existe = db.query(Roles).filter(Roles.rol_name == "admin").first()
    if existe:
        return
    
    nuevo = Roles(
        rol_name="admin",
        status=1,
        created_at=datetime.now(),
        updated_at=datetime.now()
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
        updated_at=datetime.now()
    )
    db.add(nuevo)
    db.commit()

def obtener_roles(db: Session):
    return db.query(Roles).all()