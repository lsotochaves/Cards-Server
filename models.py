from sqlalchemy import Column, Integer, String
from db import Base

class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True)
    url = Column(String, unique=True, index=True)
    name = Column(String, index=True)
    variation = Column(String)
    edition = Column(String)
    is_foil = Column(String)
    nm_price = Column(String)
    nm_qty = Column(Integer)
    ex_price = Column(String)
    ex_qty = Column(Integer)
    vg_price = Column(String)
    vg_qty = Column(Integer)
    g_price = Column(String)
    g_qty = Column(Integer)