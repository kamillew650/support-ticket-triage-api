from typing import Annotated

from fastapi import Depends, FastAPI
from sqlmodel import Session, create_engine, select, text

from .config import settings
print(settings.db_connection_string)
engine =create_engine(str(settings.db_connection_string), pool_pre_ping=True)
print(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

@app.get("/test-db")
def test_db(session: SessionDep):
    statement = "SELECT 1;"
    return session.connection().execute(text(statement)).scalar_one()