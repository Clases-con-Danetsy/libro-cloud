from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.core.security import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# ======================
# GET CURRENT USER ID
# ======================
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Token inválido")

        return int(user_id)

    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")


# ======================
# REQUIRE ROLE
# ======================
def require_min_role(min_role_id: int):

    def role_checker(token: str = Depends(oauth2_scheme)):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

            role_id = payload.get("role")

            if role_id is None:
                raise HTTPException(401, "Token sin rol")

            if role_id > min_role_id:
                raise HTTPException(
                    status_code=403, detail="No tienes permisos suficientes"
                )

            return payload

        except JWTError:
            raise HTTPException(401, "Token inválido")

    return role_checker
