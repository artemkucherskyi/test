import pytest
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Base, Contact, Invoice
import sync_data

SQLALCHEMY_DATABASE_URL = "sqlite://"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
connection = engine.connect()
Base.metadata.create_all(bind=connection)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=connection)


class FakeModels:
    def execute_kw(self, db, uid, password, model, method, args, kwargs):
        if model == "res.partner":
            return [
                {"id": 1, "name": "Alice", "email": "alice@example.com"},
                {"id": 2, "name": "Bob", "email": "bob@example.com"},
            ]
        elif model == "account.move":
            return [
                {"id": 101, "name": "INV101", "amount_total": 100.0},
                {"id": 102, "name": "INV102", "amount_total": 200.0},
            ]
        return []


def fake_get_odoo_models():
    fake_uid = 123
    return fake_uid, FakeModels()


@pytest.fixture(autouse=True)
def override_get_odoo_models(monkeypatch):
    monkeypatch.setattr(sync_data, "get_odoo_models", fake_get_odoo_models)


@pytest.fixture(scope="function")
def db_session():
    db = TestingSessionLocal()
    yield db
    for table in reversed(Base.metadata.sorted_tables):
        db.execute(table.delete())
    db.commit()
    db.close()


def test_sync_contacts(db_session):
    sync_data.sync_contacts(db_session)
    contacts = db_session.query(Contact).all()
    assert len(contacts) == 2, "Expected 2 contacts after sync"
    alice = db_session.query(Contact).filter_by(odoo_id=1).first()
    assert alice.name == "Alice"
    assert alice.email == "alice@example.com"


def test_sync_invoices(db_session):
    sync_data.sync_invoices(db_session)
    invoices = db_session.query(Invoice).all()
    assert len(invoices) == 2, "Expected 2 invoices after sync"
    inv101 = db_session.query(Invoice).filter_by(odoo_id=101).first()
    assert inv101.number == "INV101"
    assert inv101.amount_total == 100.0


def test_sync_contacts_deletion(db_session):
    extra_contact = Contact(odoo_id=999, name="Extra", email="extra@example.com")
    db_session.add(extra_contact)
    db_session.commit()
    sync_data.sync_contacts(db_session)
    extra = db_session.query(Contact).filter_by(odoo_id=999).first()
    assert extra is None, "Extra contact should have been deleted by sync"


def test_sync_invoices_deletion(db_session):
    extra_invoice = Invoice(odoo_id=999, number="INV999", amount_total=999.0)
    db_session.add(extra_invoice)
    db_session.commit()
    sync_data.sync_invoices(db_session)
    extra = db_session.query(Invoice).filter_by(odoo_id=999).first()
    assert extra is None, "Extra invoice should have been deleted by sync"
