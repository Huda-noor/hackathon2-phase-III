"""FastAPI dependencies for database sessions and authentication."""

from typing import Generator
from sqlmodel import Session
from src.core.database import engine


def get_db() -> Generator[Session, None, None]:
    """
    Database session dependency.

    Yields:
        Session: SQLModel session

    Usage:
        @app.get("/endpoint")
        def endpoint(session: Session = Depends(get_db)):
            ...
    """
    with Session(engine) as session:
        yield session
