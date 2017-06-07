import os

from sqlalchemy import (Boolean, Column, ForeignKey, Integer, String,
                        create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()
database_dir = "models/database"
driver = "sqlite:///"
echo = False


def load_engine(database_name="default.db"):
    if not os.path.exists(database_dir) or not os.path.isdir(database_dir):
        os.mkdir(database_dir)

    database_url = driver + database_dir + "/" + database_name
    return create_engine(database_url, echo=echo)


def create_session(engine):
    Session = sessionmaker(expire_on_commit=False)
    Session.configure(bind=engine)
    return Session()


def create_tables(engine):
    Base.metadata.create_all(engine)


class DBDoesNotExistException(Exception):
    pass


class DBOverwriteExecption(Exception):
    pass


class DBAlreadyLoadedException(Exception):
    pass


class UpdateException(Exception):
    pass


class OverWriteException(Exception):
    pass
