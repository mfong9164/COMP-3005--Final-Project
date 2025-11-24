import sys
from pathlib import Path

# Add parent directory to path
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from app.base import Base
from sqlalchemy import *
from models.enums import Gender
from sqlalchemy.orm import relationship

class Trainer(Base):
    __tablename__ = "Trainer"
    email = Column(String(255), primary_key=True)
    name = Column(String(100), nullable=False)
    gender = Column(Enum(Gender), nullable=False)
    
    # One trainer can have many personal training sessions
    personal_training_sessions = relationship("PersonalTrainingSession", back_populates="trainer")
    
    # One trainer can have many group fitness classes
    group_fitness_classes = relationship("GroupFitnessClass", back_populates="trainer")
    
    # One trainer can have many availability entries
    availabilities = relationship("TrainerAvailability", back_populates="trainer")
