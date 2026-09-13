from pydantic import BaseModel, Field

class TicketResponse(BaseModel):
    title: str = Field(title="Ticket tile", max_length=255)
    description: str = Field(title="Ticket description", max_length=500)
    customer_id: int = Field(title="Customer id", max= 99999999, min=1)