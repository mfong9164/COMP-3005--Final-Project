import sys
from pathlib import Path

# Add parent directory to path
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from app.base import Base
from sqlalchemy import Column, String, ForeignKey, Enum, Integer, CheckConstraint
from models.enums import GoalType
from sqlalchemy.orm import relationship


class FitnessGoal(Base):
    __tablename__ = "FitnessGoal"
    __table_args__ = (
        CheckConstraint('amount >= 0 AND amount <= 100', name='check_amount_non_negative'),
    )

    member_email = Column(
        String(255),
        ForeignKey("Member.email"), 
        primary_key=True
    )

    goal_type = Column(
        Enum(GoalType), 
        primary_key=True
    )

    amount = Column(
        Integer,
        nullable=False
    )

    # Many fitness goals belong to one member
    member = relationship("Member", back_populates="fitness_goals")