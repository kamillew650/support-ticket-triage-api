from enum import Enum
from typing import Annotated

from fastapi import Depends
from sqlalchemy import Column, String
from sqlalchemy import Enum as SAEnum
from sqlmodel import Field, Session, SQLModel, create_engine

from .config import settings

engine = create_engine(str(settings.db_connection_string), pool_pre_ping=True)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


class TicketStatus(str, Enum):
    TODO = "reported"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    ARCHIVED = "archived"


class TicketPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class TicketCategory(str, Enum):
    BUG = "bug"
    FEATURE_REQUEST = "feature_request"
    SUPPORT = "support"
    OTHER = "other"


class Ticket(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, nullable=False)
    title: str = Field(sa_column=Column(String(255), nullable=False))
    description: str = Field(sa_column=Column(String(500), nullable=False))
    customer_id: int
    status: TicketStatus = Field(
        default=TicketStatus.TODO,
        sa_column=Column(
            SAEnum(
                TicketStatus,
                name="ticket_status",
                values_callable=lambda enum: [item.value for item in enum],
            ),
            nullable=False,
            server_default=TicketStatus.TODO.value,
        ),
    )
    priority: TicketPriority | None = Field(
        default=None,
        sa_column=Column(
            SAEnum(
                TicketPriority,
                name="ticket_priority",
                values_callable=lambda enum: [item.value for item in enum],
            )
        ),
    )
    category: TicketCategory | None = Field(
        default=None,
        sa_column=Column(
            SAEnum(
                TicketCategory,
                name="ticket_category",
                values_callable=lambda enum: [item.value for item in enum],
            )
        ),
    )
