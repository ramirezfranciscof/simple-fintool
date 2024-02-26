"""
Utility function to safely access the database.
"""

import pathlib
from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

FILE_DIRPATH = pathlib.Path(__file__).parent.resolve()
MAIN_DIRPATH = FILE_DIRPATH.parent.parent.resolve()
SQLALCHEMY_DATABASE_URL = f"sqlite:///{MAIN_DIRPATH}/sqlite.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False)


@contextmanager
def get_session() -> Generator:
    try:
        session = Session(bind=engine)
        yield session
    finally:
        session.close()
