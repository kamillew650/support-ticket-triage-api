from pydantic import BaseModel, Field


class UpdateTicketDto(BaseModel):
    title: str | None = Field(default=None, title="Ticket tile", max_length=255)
    description: str | None = Field(default=None, title="Ticket description", max_length=500)
    customer_id: int | None = Field(default=None, title="Customer id", ge=1, le=99999999)