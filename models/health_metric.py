import sys
from pathlib import Path

# Add parent directory to path
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from app.base import Base
from sqlalchemy import Column, String, ForeignKey, DateTime, func

class HealthMetric(Base):
    __tablename__ = 'HealthMetric'

    member_email = Column(
        String,
        ForeignKey("Member.email"), 
        primary_key=True
    )

    created = Column(
        DateTime,
        primary_key=True,
        server_default=func.now()
    )