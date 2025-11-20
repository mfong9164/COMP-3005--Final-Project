import sys
from pathlib import Path

# Add parent directory to path
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from app.base import Base
from sqlalchemy import *

class ParticipatesIn(Base):
    __tablename__ = "ParticipatesIn"
    member_email = Column(String, ForeignKey("Member.email"), primary_key=True)
    class_id = Column(Integer, ForeignKey("GroupFitnessClass.id"), primary_key=True)
