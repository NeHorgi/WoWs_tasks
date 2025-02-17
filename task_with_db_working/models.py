from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Ship(Base):
    __tablename__ = 'ships'
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    weapon = Column(String)
    hull = Column(String)
    engine = Column(String)


class Weapon(Base):
    __tablename__ = 'weapons'
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    damage = Column(Integer)
    range = Column(Integer)
    reload_time = Column(Integer)


class Hull(Base):
    __tablename__ = 'hulls'
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    armor = Column(Integer)
    capacity = Column(Integer)


class Engine(Base):
    __tablename__ = 'engines'
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    power = Column(Integer)
    speed = Column(Integer)
