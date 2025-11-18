from main import Base
from sqlalchemy import *

class Member(Base):
    __tablename__ = "Member"
    email = Column(Integer, primary_key=True, NotNull, Unique)
    name = Column(String, NotNull)
    date_of_birth = Column(Date, NotNull)
    gender = Column(String, NotNull)
    phone_number = Column(String, NotNull)
    

