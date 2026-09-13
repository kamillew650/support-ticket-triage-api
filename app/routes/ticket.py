from app.db import SessionDep, get_session
from typing import Annotated

from app.dtos.create_ticket import CreateTicketDto
from fastapi import APIRouter, Body, Depends
from app.services.ticket_service import TicketService, get_ticket_service, TicketServiceDep

router = APIRouter(prefix="/router")

@router.post("/")
def create_ticket(data: Annotated[CreateTicketDto, Body(ember=True)], ticket_service: TicketServiceDep):
    ticket = ticket_service.create_ticket(data)
    return ticket


@router.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}