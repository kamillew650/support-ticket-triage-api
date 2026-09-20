from typing import Annotated

from fastapi import APIRouter, Body

from app.dtos.create_ticket import CreateTicketDto
from app.services.ticket_service import TicketServiceDep

from app.dtos.update_ticket import UpdateTicketDto
from app.dtos.update_ticket_status import UpdateTicketStatusDto



router = APIRouter(prefix="/ticket")

@router.get("/{ticket_id}")
def get_ticket_by_id(ticket_id: int, ticket_service: TicketServiceDep):
    return ticket_service.get_ticket_by_id(ticket_id)

@router.get("/")
def get_paginated_tickets(ticket_service: TicketServiceDep, page: int = 1, per_page: int = 10, ):
    return ticket_service.get_pagineted_tickets(page, per_page)

@router.post("/")
def create_ticket(data: Annotated[CreateTicketDto, Body(ember=True)], ticket_service: TicketServiceDep):
    ticket = ticket_service.create_ticket(data)
    return ticket

@router.patch("/{ticket_id}")
def update_ticket(ticket_id: int, data: Annotated[UpdateTicketDto, Body(ember=True)], ticket_service: TicketServiceDep):
    ticket = ticket_service.update_ticket(ticket_id, data)
    return ticket

@router.patch("/{ticket_id}/status")
def update_ticket_status(ticket_id: int, data: Annotated[UpdateTicketStatusDto, Body(ember=True)], ticket_service: TicketServiceDep):
    ticket = ticket_service.update_ticket_status(ticket_id, data)
    return ticket