from enum import Enum


class OrderBy(Enum):
    id = "id"
    title = "title"
    description = "description"
    customer_id = "customer_id"
    status = "status"