import sys
from pathlib import Path

# Add parent directory to path
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from app.base import Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

class Admin(Base):
    __tablename__ = "Admin"

    email = Column(
        String, 
        primary_key=True
    
    )
    name = Column(
        String, 
        nullable=False
    )

    # One admin can create many bills
    bills = relationship("Bill", back_populates="admin")

    # One admin can create many maintenance tickets
    maintenance_tickets = relationship("MaintenanceTicket", back_populates="admin")