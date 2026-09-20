from pydantic import BaseModel, Field

from app.dtos.ticket_response import TicketResponse


class TicketPaginatedResponse(BaseModel):
    total_pages: int = Field(title="Total pages")
    tickets: list[TicketResponse]