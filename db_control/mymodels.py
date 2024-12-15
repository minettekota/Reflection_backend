from sqlalchemy import Column, Integer, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Reflection(Base):
    __tablename__ = 'reflections'
    refleid = Column(Integer, primary_key=True, autoincrement=True)
    feeling = Column(Text, nullable=False)
    event = Column(Text, nullable=False)
    emotion = Column(Text, nullable=False)
    values = Column(Text, nullable=False)
    assess = Column(Integer, nullable=True)
    awareness = Column(Text, nullable=True)

 