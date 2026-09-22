from fastapi.testclient import TestClient


def test_missing_get_ticket_by_id(client: TestClient):
    response = client.get("/ticket/999")
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Ticket not found"

def test_get_ticket_by_id(client: TestClient):
    create_response = client.post("/ticket", json={"title": "Title", "description": "Description", "customer_id": 10})
    id = create_response.json()["id"]

    response = client.get(f"/ticket/{id}")

    assert response.status_code == 200
    assert response.json()["title"] == "Title"
    assert response.json()["description"] == "Description"
    assert response.json()["customer_id"] == 10
    assert response.json()["status"] == "reported"
    assert response.json()["id"] != None

def test_get_paginated_tickets(client: TestClient):
    create_response = client.post("/ticket", json={"title": "Title", "description": "Description", "customer_id": 10})
    assert create_response.status_code == 200

    response = client.get("/ticket")

    assert response.status_code == 200
    assert response.json()["total_pages"] == 1
    assert response.json()["tickets"][0]["title"] == "Title"
    assert response.json()["tickets"][0]["description"] == "Description"
    assert response.json()["tickets"][0]["customer_id"] == 10
    assert response.json()["tickets"][0]["status"] == "reported"
    assert response.json()["tickets"][0]["id"] != None

def test_create_ticket(client: TestClient):
    response = client.post("/ticket", json={"title": "Title", "description": "Description", "customer_id": 10})
    
    assert response.status_code == 200
    assert response.json()["title"] == "Title"
    assert response.json()["description"] == "Description"
    assert response.json()["customer_id"] == 10
    assert response.json()["status"] == "reported"
    assert response.json()["id"] != None

def test_update_ticket(client: TestClient):
    create_response = client.post("/ticket", json={"title": "Title", "description": "Description", "customer_id": 10})
    id = create_response.json()["id"]

    response = client.patch(f"/ticket/{id}", json={"title": "Title2", "description": "Description2", "customer_id": 11})

    assert response.status_code == 200
    assert response.json()["title"] == "Title2"
    assert response.json()["description"] == "Description2"
    assert response.json()["customer_id"] == 11
    assert response.json()["status"] == "reported"
    assert response.json()["id"] != None

def test_update_ticket_status(client: TestClient):
    create_response = client.post("/ticket", json={"title": "Title", "description": "Description", "customer_id": 10})
    id = create_response.json()["id"]

    response = client.patch(f"/ticket/{id}/status", json={"status": "done"})

    assert response.status_code == 200
    assert response.json()["title"] == "Title"
    assert response.json()["description"] == "Description"
    assert response.json()["customer_id"] == 10
    assert response.json()["status"] == "done"
    assert response.json()["id"] != None


