import math
from typing import Annotated, Literal

from fastapi import Depends, HTTPException
from sqlmodel import col, func, select

from app.db.session import SessionDep
from app.db.ticket import Ticket
from app.schemas.create_ticket import CreateTicketDto
from app.schemas.ticket_paginated_response import TicketPaginatedResponse
from app.schemas.ticket_response import TicketResponse
from app.schemas.update_ticket import UpdateTicketDto
from app.schemas.update_ticket_status import UpdateTicketStatusDto
from app.utils.order_by import OrderBy


class TicketService:
    def __init__(self, session: SessionDep):
        self.session = session

    def create_ticket(self, data: CreateTicketDto) -> TicketResponse:
        ticket = Ticket(
            title=data.title, description=data.description, customer_id=data.customer_id
        )
        self.session.add(ticket)
        self.session.commit()
        self.session.refresh(ticket)

        return TicketResponse.model_validate(ticket)

    def update_ticket(self, ticket_id: int, data: UpdateTicketDto):
        get_ticket_statement = select(Ticket).where(Ticket.id == ticket_id).limit(1)
        ticket = self.session.exec(get_ticket_statement).first()

        if ticket == None:
            raise HTTPException(status_code=404, detail="Ticket not found")

        updates = data.model_dump(exclude_none=True)
        ticket.sqlmodel_update(updates)
        self.session.commit()

        return TicketResponse.model_validate(ticket)
        
    
    def update_ticket_status(self, ticket_id: int, data: UpdateTicketStatusDto):
        get_ticket_statement = select(Ticket).where(Ticket.id == ticket_id).limit(1)
        ticket = self.session.exec(get_ticket_statement).first()

        if ticket == None:
            raise HTTPException(status_code=404, detail="Ticket not found")

        ticket.status = data.status
        self.session.commit()

        return TicketResponse.model_validate(ticket)

    def get_ticket_by_id(self, ticket_id: int) -> TicketResponse:
        statement = select(Ticket).where(Ticket.id == ticket_id).limit(1)
        ticket = self.session.exec(statement).first()
        if ticket == None:
            raise HTTPException(status_code=404, detail="Ticket not found")

        return TicketResponse.model_validate(ticket)

    def get_pagineted_tickets(
        self, page: int, per_page: int, order_by: OrderBy, order_direction: Literal["asc", "desc"]
    ) -> TicketPaginatedResponse:
        column_attr = getattr(Ticket, order_by.value)

        get_tickets_statement = (
            select(Ticket).offset((page - 1) * per_page).limit(per_page).order_by(column_attr.asc() if order_direction == "asc" else column_attr.desc())
        )
        tickets = self.session.exec(get_tickets_statement).all()

        get_count_statement = select(func.count(col(Ticket.id)))
        ticket_amount = self.session.exec(get_count_statement).one()
        total_pages = ticket_amount / per_page

        return TicketPaginatedResponse(
            total_pages=math.ceil(total_pages),
            tickets=[TicketResponse.model_validate(ticket) for ticket in tickets],
        )


def get_ticket_service(session: SessionDep):
    return TicketService(session)


TicketServiceDep = Annotated[TicketService, Depends(get_ticket_service)]
