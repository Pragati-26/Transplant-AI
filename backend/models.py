from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"

    id               = Column(Integer, primary_key=True, index=True)
    email            = Column(String, unique=True, index=True, nullable=False)
    username         = Column(String, unique=True, index=True, nullable=False)
    hashed_password  = Column(String, nullable=False)
    created_at       = Column(DateTime, default=datetime.utcnow)
    is_active        = Column(Integer, default=1)

    matches = relationship("Match", back_populates="user")


class Match(Base):
    __tablename__ = "matches"

    id                  = Column(Integer, primary_key=True, index=True)
    user_id             = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at          = Column(DateTime, default=datetime.utcnow)

    patient_age         = Column(Integer)
    patient_weight      = Column(Float)
    patient_bmi         = Column(Float)
    patient_blood_type  = Column(String)
    donor_age           = Column(Integer)
    donor_weight        = Column(Float)
    donor_blood_type    = Column(String)
    donor_min_age       = Column(Integer)
    donor_max_age       = Column(Integer)
    donor_min_weight    = Column(Integer)
    donor_max_weight    = Column(Integer)
    health_score        = Column(Float)
    biological_markers  = Column(Float)
    survival_chance     = Column(Float)

    compatibility_score = Column(Float)
    recommendation      = Column(String)
    explanation         = Column(Text)

    user = relationship("User", back_populates="matches")