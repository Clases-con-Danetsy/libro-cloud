from sqlalchemy.orm import Session
from datetime import datetime
from werkzeug.security import generate_password_hash
from app.models import Usuario, Roles

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
        return "El usuario ya existe"
    rol_obj = db.query(Roles).filter(Roles.id == rol).first()
    if not rol_obj:
        return "El rol no existe"
    if rol_obj.status != 1:
        return "El rol existe pero está inactivo"
    
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
    return "Usuario creado correctamente"
def obtener_usuarios(db: Session):
    return db.query(Usuario).all()
def obtener_usuario(db: Session, username: str):
    return db.query(Usuario).filter(Usuario.username == username).first()
def update_usuario(db: Session, old_username: str, new_username: str, new_rol: int):
    usuario = db.query(Usuario).filter(Usuario.username == old_username).first()
    if usuario:
        rol_obj = db.query(Roles).filter(Roles.id == new_rol).first()
        if not rol_obj:
            return "El rol no existe"
        if rol_obj.status != 1:
            return "El rol existe pero está inactivo"
        usuario.username = new_username
        usuario.updated_at = datetime.now()
        usuario.rol = new_rol
        db.add(usuario)
        db.commit()
    return "Usuario actualizado correctamente"
def delete_usuario(db: Session, username: str):
    usuario = db.query(Usuario).filter(Usuario.username == username).first()
    if usuario:
        usuario.status = 0
        usuario.updated_at = datetime.now()
        db.add(usuario)
        db.commit()
    return "Usuario eliminado correctamente"
def activate_usuario(db: Session, username: str):
    usuario = db.query(Usuario).filter(Usuario.username == username).first()
    if usuario:
        usuario.status = 1
        usuario.updated_at = datetime.now()
        db.add(usuario)
        db.commit()
    return "Usuario activado correctamente"