import sys
from pathlib import Path

# Add parent directory to path
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from app.base import Base
from sqlalchemy import *
from sqlalchemy.orm import relationship

class MaintenanceTicket(Base):
    __tablename__ = "MaintenanceTicket"
    id = Column(Integer, primary_key=True, autoincrement=True)
    admin_email = Column(String(255), ForeignKey("Admin.email"), nullable=False)
    equipment_id = Column(Integer, ForeignKey("Equipment.equipment_id"), nullable = False)
    ## Maybe change this to a int or enum?
    description = Column(Text, nullable = False)

    ## True for completed, false for not completed
    completed = Column(Boolean, nullable = False, default = False) 

    # Many tickets can be created by one admin
    admin = relationship("Admin", back_populates="maintenance_tickets")

    # Many tickets can refer to one equipment item
    equipment = relationship("Equipment", back_populates="maintenance_tickets")
