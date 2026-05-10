"""
HealthLink Kenya — SQLAlchemy ORM Models
Aligned with thesis Chapter 4 data structures and frontend data shape.
"""
from sqlalchemy import Column, String, Integer, Float, Enum, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    """Social workers, supervisors, and system administrators."""
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    role = Column(Enum("social_worker", "supervisor", name="role_enum"))
    sub_county = Column(String)
    phone = Column(String)

    # Relationship to assigned patients
    patients = relationship("Patient", back_populates="assigned_worker")


class Patient(Base):
    """
    Patient household record — maps to the KNBS survey analytical dataset.
    Fields aligned with the frontend PATIENTS array and thesis feature set.
    """
    __tablename__ = "patients"
    id = Column(String, primary_key=True)           # e.g. HH-NK-01100
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

    # ── Extended fields (thesis + frontend alignment) ─────────────
    dropout_score = Column(Float, default=0.0)      # Stage 2 retention model output
    access_score = Column(Float, default=0.0)       # Stage 1 access model output
    visit_type = Column(String, default="Regular")   # Regular, Urgent, Resolved
    nearest_facility = Column(String)
    contact_name = Column(String)
    contact_phone = Column(String)
    notes = Column(Text)                             # Clinical notes

    # Relationship back to worker
    assigned_worker = relationship("User", back_populates="patients")