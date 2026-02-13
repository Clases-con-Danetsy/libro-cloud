from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repository.usuario import get_usuario_by_id

def verificar_permiso(db: Session, user_id: int, accion: str):
    """
    Verificar si el usuario tiene permiso para realizar una acción.
    
    Acciones disponibles:
    - "ver": Todos los roles (lector, editor, admin)
    - "crear": Editor y Admin
    - "editar": Editor y Admin
    - "activar_desactivar": Solo Admin
    """
    usuario = get_usuario_by_id(db, user_id)
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    rol_nombre = usuario.rol.nombre.lower() if usuario.rol else None
    
    # Todos pueden ver
    if accion == "ver":
        return True
    
    # Solo Editor y Admin pueden crear/editar
    if accion in ["crear", "editar"]:
        if rol_nombre in ["editor", "admin"]:
            return True
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"No tienes permisos para {accion}. Solo usuarios con rol Editor o Admin pueden realizar esta acción."
        )
    
    # Solo Admin puede activar/desactivar
    if accion == "activar_desactivar":
        if rol_nombre == "admin":
            return True
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para activar/desactivar. Solo usuarios con rol Admin pueden realizar esta acción."
        )
    
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="No tienes permisos para realizar esta acción."
    )