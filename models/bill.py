import sys
from pathlib import Path

# Add parent directory to path
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from app.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Float, Enum, Boolean
from models.enums import PaymentMethod


class Bill(Base):
    __tablename__ = 'Bill'

    id = Column(
        Integer, 
        primary_key=True
    )
    
    member_email = Column(
        String,
        ForeignKey("Member.email"),
        nullable = False
    )

    admin_email = Column(
        String,
        ForeignKey("Admin.email"),
        nullable=False
    )

    amount_due = Column(
        Float,
        nullable=False
    )

    payment_method = Column(
        Enum(PaymentMethod),
        nullable=False
    )

    ## True for paid, false for unpaid
    paid = Column(
        Boolean,
        nullable=False,
        default=False
    )