from sqlalchemy.orm import Session
from app.core.security import hash_password, verify_password
from app.models import Usuario, Rol


def crear_usuario_inicial(db: Session):

    # ✅ Crear rol Admin
    rol_admin = db.query(Rol).filter(Rol.nombre == "admin").first()
    if not rol_admin:
        rol_admin = Rol(nombre="admin", status=True, created_by=1, updated_by=1)
        db.add(rol_admin)
        db.commit()
        db.refresh(rol_admin)

    # ✅ Crear rol Editor
    rol_editor = db.query(Rol).filter(Rol.nombre == "editor").first()
    if not rol_editor:
        rol_editor = Rol(nombre="editor", status=True, created_by=1, updated_by=1)
        db.add(rol_editor)
        db.commit()
        db.refresh(rol_editor)

    # ✅ Crear rol Lector
    rol_lector = db.query(Rol).filter(Rol.nombre == "lector").first()
    if not rol_lector:
        rol_lector = Rol(nombre="lector", status=True, created_by=1, updated_by=1)
        db.add(rol_lector)
        db.commit()
        db.refresh(rol_lector)

    # Usuario test (admin)
    usuario_test = db.query(Usuario).filter(Usuario.username == "test").first()
    password_hash = hash_password("123456")

    if usuario_test:
        usuario_test.password = password_hash
        usuario_test.status = True  
        if usuario_test.rol_id != rol_admin.id:  # ✅ CORREGIDO: rol_id
            usuario_test.rol_id = rol_admin.id  # ✅ CORREGIDO: rol_id
        db.commit()
    else:
        nuevo = Usuario(
            username="test",
            password=password_hash,
            rol_id=rol_admin.id,  # ✅ CORREGIDO: rol_id
            status=True,
            created_by=1,
            updated_by=1
        )
        db.add(nuevo)
        db.commit()

def create_usuario(db: Session, username: str, password: str, rol_id: int, created_by: int, updated_by: int):
    rol = db.query(Rol).filter(Rol.id == rol_id).first()
    if not rol:
        raise ValueError("El rol especificado no existe.")

    if hasattr(rol, "status") and rol.status != True:
        raise ValueError("El rol especificado no está activo.")

    hashed_password = hash_password(password)
    nuevo_usuario = Usuario(
        username=username,
        password=hashed_password,
        rol_id=rol_id,
        status=True,
        created_by=created_by,
        updated_by=updated_by
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario


def get_usuario_by_username(db: Session, username: str):
    return db.query(Usuario).filter(Usuario.username == username).first()


def get_usuario_by_id(db: Session, id: int):
    return db.query(Usuario).filter(Usuario.id == id).first()


def update_usuario(
    db: Session,
    user_id: int,
    username: str = None,
    rol_id: int = None,
    status: bool = None,
    updated_by: int = None,
):
    usuario_db = db.query(Usuario).filter(Usuario.id == user_id).first()
    if not usuario_db:
        return None

    if rol_id is not None:
        rol = db.query(Rol).filter(Rol.id == rol_id).first()
        if not rol:
            raise ValueError("El rol especificado no existe.")
        if hasattr(rol, "status") and rol.status != True:
            raise ValueError("El rol especificado no está activo.")
        usuario_db.rol_id = rol_id

    if username is not None:
        usuario_db.username = username

    if status is not None:
        usuario_db.status = status

    if updated_by is not None:
        usuario_db.updated_by = updated_by

    db.commit()
    db.refresh(usuario_db)
    return usuario_db


def delete_usuario(db: Session, user_id: int, id_user: int):
    usuario_db = db.query(Usuario).filter(Usuario.id == user_id).first()
    if not usuario_db:
        return None
    usuario_db.status = False  
    usuario_db.updated_by = id_user
    db.commit()
    db.refresh(usuario_db)
    return usuario_db


def activate_usuario(db: Session, user_id: int, id_user: int):
    usuario_db = db.query(Usuario).filter(Usuario.id == user_id).first()
    if not usuario_db:
        return None

    usuario_db.status = True
    usuario_db.updated_by = id_user

    db.commit()
    db.refresh(usuario_db)
    return usuario_db


def login_usuario(db: Session, username: str, password: str):
    usuario = get_usuario_by_username(db, username)
    if not usuario:
        raise ValueError("Usuario no encontrado")

    if not verify_password(password, usuario.password):
        raise ValueError("Contraseña incorrecta")

    if usuario.status != True:
        raise ValueError("Usuario no está activo")

    rol_nombre = usuario.rol.nombre if usuario.rol else None

    return {
        "id": usuario.id,
        "username": usuario.username,
        "role_id": usuario.rol_id,
        "rol_name": rol_nombre,

    }
    
def get_users_by_ids(db: Session, ids: list[int]):
    if not ids:
        return []
    return db.query(Usuario).filter(Usuario.id.in_(ids)).all()

