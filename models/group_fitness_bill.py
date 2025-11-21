import sys
from pathlib import Path

# Add parent directory to path
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from app.base import Base
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

class GroupFitnessBill(Base):
    __tablename__ = "GroupFitnessBill"

    bill_id = Column(
        Integer,
        ForeignKey("Bill.id"),
        primary_key = True,
    )

    class_id = Column(
        Integer,
        ForeignKey("GroupFitnessClass.id"),
        primary_key = True
    )

    # Many group fitness bill links belong to one bill
    bill = relationship("Bill", back_populates="group_fitness_bills")

    # Many group fitness bill links belong to one fitness class
    fitness_class = relationship("GroupFitnessClass", back_populates="group_fitness_bills")