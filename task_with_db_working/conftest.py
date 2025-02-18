import random
import tempfile
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import get_session
from models import Ship, Weapon, Hull, Engine
from task_with_db_working.constants import random_value


@pytest.fixture(scope="session")
def db_session():
    """
    Get original database session.
    """
    session = get_session()
    yield session
    session.close()


@pytest.fixture(scope="session")
def temp_db_session(db_session):
    """
    Get temporary database session.

    :param db_session: Original database session.
    """
    temp_db_path = tempfile.mktemp(suffix=".db")
    engine = create_engine(f"sqlite:///{temp_db_path}")
    session = sessionmaker(bind=engine)
    temp_session = session()

    from database import Base

    Base.metadata.create_all(engine)
    fill_temp_db(temp_session, db_session)
    randomize_db(temp_session)

    yield temp_session
    temp_session.close()


def fill_temp_db(temp_session, original_session):
    """
    Method fills temporary database by taking writes from original database.

    :param temp_session: Temporary database session.
    :param original_session: Original database session.
    """
    for model in [Weapon, Hull, Engine, Ship]:
        records = original_session.query(model).all()
        for record in records:
            temp_session.merge(record)
    temp_session.commit()


def randomize_db(session):
    """
    Method randomizing writes in given database.
    For all ships in database it randomizes writes by changing one of modules of the ship.
    And for all ships it also randomizes one random value for all modules in database.
    Randomizing values by choosing random value from 1 to 20.

    :param session: Database session.
    """
    weapons = [weapon for weapon in session.query(Weapon).all()]
    hulls = [hull for hull in session.query(Hull).all()]
    engines = [engine for engine in session.query(Engine).all()]

    ships = session.query(Ship).all()

    for ship in ships:
        field_to_change = random.choice(["weapon", "hull", "engine"])

        if field_to_change == "weapon":
            new_value = random.choice([weapon.id for weapon in weapons])
        elif field_to_change == "hull":
            new_value = random.choice([hull.id for hull in hulls])
        else:
            new_value = random.choice([engine.id for engine in engines])

        setattr(ship, field_to_change, new_value)

    for models in [weapons, hulls, engines]:
        for model in models:
            attrs = [key for key, value in model.__dict__.items() if type(value) == int]
            setattr(model, random.choice(attrs), random_value())

    session.commit()
