import sys
from pathlib import Path

# Add parent directory to path
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from app.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Float, Enum, Boolean
import enum

class PaymentMethod(enum.Enum):
    CASH = 0
    DEBIT = 1
    CREDIT = 2

class Bill(Base):
    __tablename__ = 'Bill'

    id = Column(
        Integer, primary_key=True
    )
    
    member_email = Column(
        String,
        ForeignKey("Member.email"), 
        primary_key=True
    )

    admin_email = Column(
        String,
        ForeignKey("AdminStaff.email")
    )

    amount_due = Column(
        Float,
        nullable=False
    )

    payment_method = Column(
        Enum(PaymentMethod),
        nullable=False
    )

    status = Column(
        Boolean,
        nullable=False,
        default=False
    )