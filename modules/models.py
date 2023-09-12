from sqlalchemy import Column, Float, Integer, String, Date
from modules.database import Base


class Orders(Base):
    __tablename__ = "data"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    date = Column(Date)
    associate = Column(String)
    unita = Column(Float)
    unitb = Column(Float)
    unitc = Column(Float)
    unitd = Column(Float)
    unite = Column(Float)
    unitf = Column(Float)
    unitg = Column(Float)
    unith = Column(Float)
   

class Users(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    login = Column(String)
    fname = Column(String)
    lname = Column(String)
    password = Column(String)
    lvl = Column(Integer)   