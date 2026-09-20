from app.db import TicketStatus
from pydantic import BaseModel, Field


class UpdateTicketStatusDto(BaseModel):
    status: TicketStatus = Field(title="Ticket status")