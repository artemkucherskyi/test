import os
import sys
import warnings
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

warnings.filterwarnings(
    "ignore", message="Deprecated API features detected", category=UserWarning
)

from models import Base, Contact, Invoice
from main import app, get_db

SQLALCHEMY_DATABASE_URL = "sqlite://"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
connection = engine.connect()
Base.metadata.create_all(bind=connection)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=connection)


@pytest.fixture(autouse=True)
def override_get_db():
    def _get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = _get_db


@pytest.fixture(scope="function")
def populate_data():
    db = TestingSessionLocal()
    contact1 = Contact(odoo_id=1, name="Test Contact 1", email="contact1@example.com")
    contact2 = Contact(odoo_id=2, name="Test Contact 2", email="contact2@example.com")
    db.add_all([contact1, contact2])
    invoice1 = Invoice(odoo_id=101, number="INV101", amount_total=100.0)
    invoice2 = Invoice(odoo_id=102, number="INV102", amount_total=200.0)
    db.add_all([invoice1, invoice2])
    db.commit()
    yield
    for table in reversed(Base.metadata.sorted_tables):
        db.execute(table.delete())
    db.commit()
    db.close()


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as c:
        yield c
