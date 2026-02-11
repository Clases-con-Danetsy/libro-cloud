from datetime import datetime, timedelta
from jose import jwt, JWTError
from pwdlib import PasswordHash

SECRET_KEY = "SUPER_SECRET_KEY_CAMBIALA"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# 🔐 Hash moderno (Argon2 recomendado)
password_hash = PasswordHash.recommended()


# =========================
# PASSWORD
# =========================
def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return password_hash.verify(plain, hashed)


# =========================
# JWT
# =========================
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
