import sys
from pathlib import Path

# Add parent directory to path
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from app.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Float, Enum, Boolean, CheckConstraint
from models.enums import PaymentMethod
from sqlalchemy.orm import relationship

class Bill(Base):
    __tablename__ = 'Bill'
    __table_args__ = (
        CheckConstraint('amount_due >= 0', name='check_amount_non_negative'),
    )

    id = Column(
        Integer, 
        primary_key=True,
        autoincrement=True
    )
    
    member_email = Column(
        String(255),
        ForeignKey("Member.email"),
        nullable = False
    )

    admin_email = Column(
        String(255),
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
    
    # Many bills can belong to one member
    member = relationship("Member", back_populates="bills")
    
    # Many bills can be processed by one admin
    admin = relationship("Admin", back_populates="bills")
    
    # One bill can be linked to many personal training sessions via PersonalTrainingBill
    personal_training_bills = relationship("PersonalTrainingBill", back_populates="bill")
    
    # One bill can be linked to many group fitness classes via GroupFitnessBill
    group_fitness_bills = relationship("GroupFitnessBill",back_populates="bill")