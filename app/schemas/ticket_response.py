from pydantic import BaseModel, ConfigDict, Field

from app.db.ticket import TicketCategory, TicketPriority, TicketStatus


class TicketResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(title="Ticket id")
    title: str = Field(title="Ticket tile", max_length=255)
    description: str = Field(title="Ticket description", max_length=500)
    customer_id: int = Field(title="Customer id", le= 99999999, ge=1)
    status: TicketStatus | None = None
    priority: TicketPriority | None = None
    category: TicketCategory | None = None