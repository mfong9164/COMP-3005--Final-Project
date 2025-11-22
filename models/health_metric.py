import sys
from pathlib import Path

# Add parent directory to path
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from app.base import Base
from sqlalchemy import *
from sqlalchemy.orm import relationship

class HealthMetric(Base):
    __tablename__ = 'HealthMetric'
    __table_args__ = (
        CheckConstraint('height > 0', name='check_height_positive'),
        CheckConstraint('weight > 0', name='check_weight_positive'),
        CheckConstraint('heart_rate > 0 AND heart_rate <= 300', name='check_heart_rate_valid'),
    )

    member_email = Column(
        String(255),
        ForeignKey("Member.email"), 
        primary_key=True
    )

    created = Column(
        DateTime,
        primary_key=True,
        server_default=func.now()
    )
    
    height = Column(Float, nullable = False)

    weight = Column(Float, nullable = False)

    heart_rate = Column(Integer, nullable = False)

    # Many health metric records belong to one member
    member = relationship("Member", back_populates="health_metrics")