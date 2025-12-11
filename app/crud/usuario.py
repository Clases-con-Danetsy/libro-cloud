from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash
from app.models import Usuario

def crear_usuario_inicial(db: Session):
    existe = db.query(Usuario).filter(Usuario.username == "test").first()
    if existe:
        return
    
    nuevo = Usuario(
        username="test",
        password=generate_password_hash("123"),
        rol="admin"
    )
    db.add(nuevo)
    db.commit()
