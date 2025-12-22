from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash
from app.models import Usuario, Rol

def crear_usuario_inicial(db: Session):
    existe = db.query(Usuario).filter(Usuario.username == "test").first()
    if existe:
        return
    
    # Verificar si existe el rol admin
    rol_admin = db.query(Rol).filter(Rol.nombre == "admin").first()
    if not rol_admin:
        rol_admin = Rol(nombre="admin")
        db.add(rol_admin)
        db.commit()
        db.refresh(rol_admin)

    nuevo = Usuario(
        username="test",
        password=generate_password_hash("123"),
        role_id=rol_admin.id
    )
    db.add(nuevo)
    db.commit()

def create_usuario(db: Session, username: str, password: str, role_id: int):
    hashed_password = generate_password_hash(password)
    nuevo_usuario = Usuario(username=username, password=hashed_password, role_id=role_id)
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

def get_usuario_by_username(db: Session, username: str):
    return db.query(Usuario).filter(Usuario.username == username).first()
