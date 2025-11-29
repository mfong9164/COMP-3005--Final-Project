import sys
from pathlib import Path

# Add parent directory to path
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from app.base import Base
from sqlalchemy import *
from models.enums import Gender
from sqlalchemy.orm import relationship
from sqlalchemy import UniqueConstraint

class Member(Base):
    __tablename__ = "Member"
    email = Column(String(255), primary_key=True, unique=True)
    name = Column(String(100), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(Enum(Gender), nullable=False)
    phone_number = Column(String(10), nullable=False)

    # One member can have many bills
    # lazy='select' means the bills will be loaded with a separate query when accessed (lazy loading)
    # this avoids loading bills if they are not needed, saving database queries
    bills = relationship("Bill", back_populates = "member", lazy='select')

    # One member can have many health metrics
    # lazy='select' means health metrics load on access with a separate query
    health_metrics = relationship("HealthMetric", back_populates="member", lazy='select')
    
    # One member can have many fitness goals
    # lazy='select' means fitness goals load on access with a separate query
    fitness_goals = relationship("FitnessGoal", back_populates="member", lazy='select')
    
    # One member can have many personal training sessions
    # lazy='select' means personal training sessions load on access with a separate query
    personal_training_sessions = relationship("PersonalTrainingSession", back_populates="member", lazy='select')

    # One member can have many participation records for group fitness classes
    # lazy='select' means participations load on access with a separate query
    participations = relationship("ParticipatesIn", back_populates="member", lazy='select')
