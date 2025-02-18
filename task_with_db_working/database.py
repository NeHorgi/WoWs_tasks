from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.engine import Engine
from models import Base
from task_with_db_working.constants import constants


def create_database(db_path: str = constants.db_path) -> Engine:
    """
    Creates SQLite database by given path and creates tables.

    :param db_path: Path to database.
    :return: Engine obj of database.
    """
    engine = create_engine(db_path)
    Base.metadata.create_all(engine)
    return engine


def get_session(db_path: str = constants.db_path) -> Session:
    """
    Creates session for work with database by given path.

    :param db_path: Path to database.
    :return: Session obj of database.
    """
    engine = create_engine(db_path)
    session = sessionmaker(bind=engine)
    return session()
