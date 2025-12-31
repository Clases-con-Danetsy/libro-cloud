from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base
from datetime import datetime

class Roles(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    rol_name = Column(String(50), unique=True, nullable=False)
    status = Column (Integer, nullable = False, default=1)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    updated_at = Column(DateTime, nullable=False, default=datetime.now())