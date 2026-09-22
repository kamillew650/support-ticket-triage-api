# Support Ticket Triage API

A learning project for building Python APIs with FastAPI, SQLModel, PostgreSQL,
and Alembic. It supports creating, reading, updating, and sorting support tickets.
AI-powered classification is planned but not implemented yet.

## Local setup

Requires Python 3.14+, uv, and Docker with Docker Compose. Run commands from the
project root.

1. Install dependencies, including development tools:

   ```bash
   uv sync
   ```

2. Create a `.env` file containing the connection string for the local Docker database:

   ```dotenv
   DB_CONNECTION_STRING=postgresql+psycopg2://postgres:postgres@localhost:5432/support_ticket_triage
   ```

3. Start PostgreSQL and wait until it is ready:

   ```bash
   docker compose up -d db
   docker compose exec db pg_isready -U postgres -d support_ticket_triage
   ```

4. Apply database migrations:

   ```bash
   uv run alembic upgrade head
   ```

   **Current refactor issue:** migrations fail because `alembic/env.py` still
   imports `Ticket` from its previous location. This must be resolved before
   migrations can run.

5. Start the development server:

   ```bash
   uv run uvicorn app.main:app --reload
   ```

Open the interactive API documentation at <http://127.0.0.1:8000/docs>.

## Endpoints

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/health` | Check that the API is running |
| POST | `/ticket/` | Create a ticket |
| GET | `/ticket/` | List tickets with pagination and sorting |
| GET | `/ticket/{ticket_id}` | Read a ticket |
| PATCH | `/ticket/{ticket_id}` | Update ticket fields |
| PATCH | `/ticket/{ticket_id}/status` | Update ticket status |

Listing accepts `page`, `per_page` (1–20), `order_by`, and `order_direction`
(`asc` or `desc`). PATCH preserves omitted fields and ignores explicit `null` values.

## Tests and checks

Run the tests with an isolated, in-memory SQLite database. PostgreSQL and Docker
are not needed for these tests, and PostgreSQL migrations are not exercised.

```bash
DB_CONNECTION_STRING=sqlite:// uv run python -m pytest -v
```

Run linting, formatting verification, and type checking:

```bash
uv run ruff check .
uv run ruff format --check .
uv run ty check .
```

## Project layout

- `app/main.py`: application entry point.
- `app/routes/`: HTTP endpoints.
- `app/services/`: ticket operations.
- `app/schemas/`: request and response models.
- `app/db/`: database session setup, table models, and ticket enums.
- `app/config.py`: environment-based settings.
- `app/utils/`: sorting options.
- `alembic/`: database migrations.
- `tests/`: API tests and shared fixtures.
