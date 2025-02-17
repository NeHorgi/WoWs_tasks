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
    session = get_session()
    yield session
    session.close()


@pytest.fixture(scope="session")
def temp_db_session(db_session):
    temp_db_path = tempfile.mktemp(suffix=".db")
    engine = create_engine(f"sqlite:///{temp_db_path}")
    session = sessionmaker(bind=engine)
    temp_session = session()

    from database import Base

    Base.metadata.create_all(engine)
    fill_temp_db(temp_session, db_session)

    yield temp_session
    temp_session.close()


def fill_temp_db(temp_session, original_session):
    for model in [Weapon, Hull, Engine, Ship]:
        records = original_session.query(model).all()
        for record in records:
            temp_session.merge(record)
    temp_session.commit()


def randomize_temp_db(session):
    weapons = [weapon.id for weapon in session.query(Weapon).all()]
    hulls = [hull.id for hull in session.query(Hull).all()]
    engines = [engine.id for engine in session.query(Engine).all()]

    ships = session.query(Ship).all()

    for ship in ships:
        field_to_change = random.choice(["weapon", "hull", "engine"])
        old_value = getattr(ship, field_to_change)

        if field_to_change == "weapon":
            new_value = random.choice(weapons)
        elif field_to_change == "hull":
            new_value = random.choice(hulls)
        else:
            new_value = random.choice(engines)

        setattr(ship, field_to_change, new_value)
        print(f"Ship {ship.id}: {field_to_change} was changed from {old_value} to {new_value}")

    session.commit()
