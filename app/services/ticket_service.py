from typing import Annotated
from fastapi import Depends
from app.db import SessionDep, Ticket, get_session
from app.dtos.create_ticket import CreateTicketDto
from app.dtos.ticket_response import TicketResponse



class TicketService:
    def __init__(self, session: SessionDep):
        self.session = session

    def create_ticket(self, data: CreateTicketDto):
        ticket = Ticket(
            title=data.title,
            description=data.description,
            customer_id=data.customer_id
        )
        self.session.add(ticket)
        self.session.commit()

        return TicketResponse(title=ticket.title, description=ticket.description, customer_id=ticket.customer_id)

def get_ticket_service(session: SessionDep):
    return TicketService(session)

TicketServiceDep = Annotated[TicketService, Depends(get_ticket_service)]
