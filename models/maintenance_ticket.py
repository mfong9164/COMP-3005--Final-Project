import sys
from pathlib import Path

# Add parent directory to path
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from app.base import Base
from sqlalchemy import *

class MaintenanceTicket(Base):
    __tablename__ = "MaintenanceTicket"
    id = Column(Integer, primary_key=True)
    admin_email = Column(String, ForeignKey("Admin.email"), nullable=False)
    equipment_id = Column(Integer, ForeignKey("Equipment.equipment_id"), nullable = False)
    ## Maybe change this to a int or enum?
    description = Column(Text, nullable = False)
