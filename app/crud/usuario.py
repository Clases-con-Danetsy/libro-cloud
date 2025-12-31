from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash, check_password_hash
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
    # Validar rol
    rol = db.query(Rol).filter(Rol.id == role_id).first()
    if not rol:
        raise ValueError("El rol especificado no existe.")
    if not rol.is_active:
        raise ValueError("El rol especificado no está activo.")

    hashed_password = generate_password_hash(password)
    nuevo_usuario = Usuario(username=username, password=hashed_password, role_id=role_id)
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

def get_usuario_by_username(db: Session, username: str):
    return db.query(Usuario).filter(Usuario.username == username).first()

def update_usuario(db: Session, user_id: int, username: str = None, role_id: int = None, is_active: bool = None):
    usuario_db = db.query(Usuario).filter(Usuario.id == user_id).first()
    if not usuario_db:
        return None

    if role_id is not None:
        rol = db.query(Rol).filter(Rol.id == role_id).first()
        if not rol:
            raise ValueError("El rol especificado no existe.")
        if not rol.is_active:
            raise ValueError("El rol especificado no está activo.")
        usuario_db.role_id = role_id

    if username is not None:
        usuario_db.username = username
    
    if is_active is not None:
        usuario_db.is_active = is_active

    db.commit()
    db.refresh(usuario_db)
    return usuario_db

def delete_usuario(db: Session, user_id: int):
    usuario_db = db.query(Usuario).filter(Usuario.id == user_id).first()
    if not usuario_db:
        return None
    usuario_db.is_active = False
    db.commit()
    db.refresh(usuario_db)
    return usuario_db

def activate_usuario(db: Session, user_id: int):
    usuario_db = db.query(Usuario).filter(Usuario.id == user_id).first()
    if not usuario_db:
        return None
    usuario_db.is_active = True
    db.commit()
    db.refresh(usuario_db)
    return usuario_db

def login_usuario(db: Session, username: str, password: str):
    usuario = get_usuario_by_username(db, username)
    if not usuario:
        raise ValueError("Usuario no encontrado")
    
    if not check_password_hash(usuario.password, password):
        raise ValueError("Contraseña incorrecta")
    
    if not usuario.is_active:
        raise ValueError("Usuario no está activo")
        
    return usuario
