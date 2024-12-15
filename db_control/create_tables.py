import platform
print(platform.uname())

from mymodels import Base #, User, Comment
from connect import engine

print("Creating tables >>> ")
Base.metadata.create_all(bind=engine)


from sqlalchemy import Column, Integer, String, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from db_control.connect import engine

Base = declarative_base()

class Reflection(Base):
    __tablename__ = 'reflection_d'
    refleid = Column(Integer, primary_key=True, autoincrement=True)
    event = Column(Text, nullable=False)
    emotion = Column(Text, nullable=False)
    opinion = Column(Text, nullable=False)
    values = Column(Text, nullable=False)
    assess = Column(Integer, nullable=True)
    awareness = Column(Text, nullable=True)

def create_tables():
    Base.metadata.create_all(engine)

if __name__ == '__main__':
    create_tables()
    print("Tables created successfully.")
