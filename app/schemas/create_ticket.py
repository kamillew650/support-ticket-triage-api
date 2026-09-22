from pydantic import BaseModel, Field


class CreateTicketDto(BaseModel):
    title: str = Field(title="Ticket tile", max_length=255)
    description: str = Field(title="Ticket description", max_length=500)
    customer_id: int = Field(title="Customer id", ge=1, le=99999999)