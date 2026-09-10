from fastapi import FastAPI

from app.routes.health_check import router as health_router
from app.routes.ticket import router as ticket_router

app = FastAPI(
    title="My API",
    version="1.0.0",
)

app.include_router(ticket_router, tags=["tickets"])
app.include_router(health_router, tags=["tickets"])
