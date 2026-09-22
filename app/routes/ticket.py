from typing import Annotated, Literal

from fastapi import APIRouter, Body, Query

from app.schemas.create_ticket import CreateTicketDto
from app.schemas.update_ticket import UpdateTicketDto
from app.schemas.update_ticket_status import UpdateTicketStatusDto
from app.services.ticket_service import TicketServiceDep
from app.utils.order_by import OrderBy

router = APIRouter(prefix="/ticket")


@router.get("/{ticket_id}")
def get_ticket_by_id(ticket_id: int, ticket_service: TicketServiceDep):
    return ticket_service.get_ticket_by_id(ticket_id)


@router.get("/")
def get_paginated_tickets(
    ticket_service: TicketServiceDep,
    page: Annotated[int, Query(ge=1)] = 1,
    per_page: Annotated[int, Query(ge=1, le=20)] = 10,
    order_by: Annotated[OrderBy, Query()] = OrderBy.id,
    order_direction: Annotated[Literal["asc", "desc"], Query(regex="^(asc|desc)$")] = "asc",
):
    return ticket_service.get_pagineted_tickets(page, per_page, order_by, order_direction)


@router.post("/")
def create_ticket(data: CreateTicketDto, ticket_service: TicketServiceDep):
    ticket = ticket_service.create_ticket(data)
    return ticket


@router.patch("/{ticket_id}")
def update_ticket(
    ticket_id: int,
    data: Annotated[UpdateTicketDto, Body(ember=True)],
    ticket_service: TicketServiceDep,
):
    ticket = ticket_service.update_ticket(ticket_id, data)
    return ticket


@router.patch("/{ticket_id}/status")
def update_ticket_status(
    ticket_id: int,
    data: Annotated[UpdateTicketStatusDto, Body(ember=True)],
    ticket_service: TicketServiceDep,
):
    ticket = ticket_service.update_ticket_status(ticket_id, data)
    return ticket
