from sqlalchemy import Column,Integer,String
from app.db.session import Base

class User(Base):
    __tablenamr__ = "user"
    id= Column(Integer, primary_key=True,index=True)
    username = Column(String(50),unique=True,index=True,nullable=False)
    email = Column(String(100),unique=True,index=True,nullable=False)
    full_name = Column(String(100),nullable=True)

    