import sys
from pathlib import Path

# Add parent directory to path
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from app.base import Base
from sqlalchemy import Column, String

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