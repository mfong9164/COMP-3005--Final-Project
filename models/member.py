import sys
from pathlib import Path

# Add parent directory to path
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from app.base import Base
from sqlalchemy import *
from models.enums import Gender
from sqlalchemy.orm import relationship

class Member(Base):
    __tablename__ = "Member"
    email = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(Enum(Gender), nullable=False)
    phone_number = Column(String, nullable=False)

    # One member can have many bills
    bills = relationship("Bill", back_populates = "member")

    # One member can have many health metrics
    health_metrics = relationship("HealthMetric", back_populates="member")
    
    # One member can have many fitness goals
    fitness_goals = relationship("FitnessGoal", back_populates="member")
    
    # One member can have many personal training sessions
    personal_training_sessions = relationship("PersonalTrainingSession", back_populates="member")

    # One member can have many participation records for group fitness classes
    participations = relationship("ParticipatesIn", back_populates="member")
