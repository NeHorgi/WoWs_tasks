from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from task_with_db_working.constants import constants


def create_database(db_path=constants.db_path):
    engine = create_engine(db_path)
    Base.metadata.create_all(engine)
    return engine


def get_session(db_path=constants.db_path):
    engine = create_engine(db_path)
    session = sessionmaker(bind=engine)
    return session()
