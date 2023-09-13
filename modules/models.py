from sqlalchemy import Column, Integer, String, Date, Boolean
from modules.database import Base


class Tasks(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user = Column(String)
    start_date = Column(Date)
    frequency = Column(Integer)
    quantity = Column(Integer)
   

class Users(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True)
    password = Column(String)
    admin = Column(Boolean)
