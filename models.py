from sqlalchemy import Boolean, Column, Integer, String
from database import Base

class Address(Base):
    __tablename__ = "address"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True, nullable=False)
    address = Column(String)
    coordinate = Column(String)
