from sqlalchemy.orm import Session
from datetime import datetime
from werkzeug.security import generate_password_hash
from app.models import Usuario

def crear_usuario_inicial(db: Session):
    existe = db.query(Usuario).filter(Usuario.username == "test").first()
    if existe:
        return
    
    nuevo = Usuario(
        username="test",
        password=generate_password_hash("123"),
        rol=1,
        status=1,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    db.add(nuevo)
    db.commit()
def crear_usuario(db: Session, username: str, password: str, rol: int):
    existe = db.query(Usuario).filter(Usuario.username == username).first()
    if existe:
        return
    
    nuevo = Usuario(
        username=username,
        password=generate_password_hash(password),
        rol=rol,
        status=1,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    db.add(nuevo)
    db.commit()

def obtener_usuarios(db: Session):
    return db.query(Usuario).all()