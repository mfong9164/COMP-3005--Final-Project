import sys
from pathlib import Path

# Add parent directory to path
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from app.base import Base
from sqlalchemy import Column, Integer, ForeignKey

class GroupFitnessBill(Base):
    __tablename__ = "GroupFitnessBill"

    bill_id = Column(
        Integer,
        ForeignKey("Bill.id"),
        primary_key=True
    )

    session_id = Column(
        Integer,
        ForeignKey("GroupFitnessClass.id"),
        primary_key=True
    )