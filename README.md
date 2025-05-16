# FastAPI Zero

FastAPI Zero is a minimalist FastAPI project template that provides a solid foundation for building RESTful APIs with Python.

## Features

- FastAPI framework for high-performance API development
- Pydantic for data validation
- SQLAlchemy for database ORM
- Alembic for database migrations
- Docker and Docker Compose support
- JWT authentication
- Pytest for testing
- Pre-configured project structure

## Project Structure

```
fastapi_zero/
├── app/
│   ├── api/
│   │   ├── deps.py
│   │   ├── endpoints/
│   │   └── routes.py
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   ├── db/
│   │   ├── base.py
│   │   └── session.py
│   ├── models/
│   ├── schemas/
│   └── main.py
├── migrations/
├── tests/
├── .env
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.8+
- Docker and Docker Compose (optional)

### Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/fastapi_zero.git
cd fastapi_zero
```

2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up environment variables:

```bash
cp .env.example .env
```

Edit the `.env` file with your configuration.

### Running the Application

#### Using Python

```bash
uvicorn app.main:app --reload
```

#### Using Docker

```bash
docker-compose up -d
```

The API will be available at http://localhost:8000

API documentation will be available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Database Migrations

Initialize migrations (first time only):

```bash
alembic init migrations
```

Create a new migration:

```bash
alembic revision --autogenerate -m "Description of changes"
```

Apply migrations:

```bash
alembic upgrade head
```

## Testing

Run tests with pytest:

```bash
pytest
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Alembic](https://alembic.sqlalchemy.org/)
- [Pydantic](https://pydantic-docs.helpmanual.io/)