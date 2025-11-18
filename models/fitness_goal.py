from sqlalchemy import Column, String, ForeignKey, Enum, Integer
from base import Base

class Type(enum.Enum):
    WEIGHT = 0
    BODY_FAT_PERCENTAGE = 1
    CARDIO = 2

class FitnessGoal(Base):
    __tablename__ = "FitnessGoal"

    member_email = Column(
        String,
        ForeignKey("Member.id"), 
        primary_key=True
    )

    type = Column(
        Enum(Type), 
        primary_key=True
    )

    amount = Column(
        Integer
    )