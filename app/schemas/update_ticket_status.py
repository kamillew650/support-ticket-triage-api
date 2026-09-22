from pydantic import BaseModel, Field

from app.db.ticket import TicketStatus


class UpdateTicketStatusDto(BaseModel):
    status: TicketStatus = Field(title="Ticket status")