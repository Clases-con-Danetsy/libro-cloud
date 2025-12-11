from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import pymysql

MYSQL_USER = "root"
MYSQL_PASS = "123456"
MYSQL_HOST = "localhost"
MYSQL_DB   = "libro_cloud"
MYSQL_PORT = 3307


# Crear la base de datos si no existe
connection = pymysql.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    password=MYSQL_PASS,
    port=int(MYSQL_PORT)
)

with connection.cursor() as cursor:
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{MYSQL_DB}`")
connection.close()


# URL con puerto incluido
DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASS}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"


engine = create_engine(
    DATABASE_URL,
    echo=True,             # muestra SQL en consola
    pool_pre_ping=True,
    pool_recycle=3600,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()
