from sqlalchemy import Column, Integer, String, Date, Boolean
from modules.database import Base


class Habits(Base):
    __tablename__ = "habits"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer)
    name = Column(String)
    icon = Column(String)
    start_date = Column(Date)
    frequency = Column(Integer)
    quantity = Column(Integer)
    weekends = Column(Integer)
   

class Users(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True)
    password = Column(String)
    language = Column(String)
    shorts = Column(Boolean)
    theme = Column(String)
    mode = Column(String)
    admin = Column(Boolean)
    active = Column(Boolean)
    

class Tasks(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer)
    name = Column(String)
    date = Column(Date)
    state = Column(Boolean)