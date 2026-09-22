from enum import Enum
from typing import Annotated

from fastapi import Depends
from sqlalchemy import Column, String
from sqlalchemy import Enum as SAEnum
from sqlmodel import Field, Session, SQLModel, create_engine

from app.config import settings

engine = create_engine(str(settings.db_connection_string), pool_pre_ping=True)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]