"""
Database tables.
"""

from sqlalchemy import Column, Double, Integer, String
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class InstrumentPriceModifier(Base):
    __tablename__ = "INSTRUMENT_PRICE_MODIFIER"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, index=True)
    multiplier = Column(Double)
