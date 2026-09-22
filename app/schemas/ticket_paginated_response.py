from pydantic import BaseModel, Field

from app.schemas.ticket_response import TicketResponse


class TicketPaginatedResponse(BaseModel):
    total_pages: int = Field(title="Total pages")
    tickets: list[TicketResponse] = Field(title="Tickets")