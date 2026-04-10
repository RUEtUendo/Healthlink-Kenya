from sqlalchemy import Column, String, Integer, Float, Enum, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    role = Column(Enum("social_worker", "supervisor", name="role_enum"))

class Patient(Base):
    __tablename__ = "patients"
    id = Column(String, primary_key=True)   # e.g. HH-NK-01100
    name = Column(String)
    age = Column(Integer)
    gender = Column(String(1))
    sub_county = Column(String)
    condition = Column(String)
    risk = Column(Enum("High", "Medium", "Low", name="risk_enum"))
    distance_km = Column(Float)
    insurance = Column(String)
    last_visit = Column(Date)
    assigned_worker_id = Column(Integer, ForeignKey("users.id"))
    latitude = Column(Float)
    longitude = Column(Float)