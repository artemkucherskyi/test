import os
import xmlrpc.client

from dotenv import load_dotenv

from models import Contact, Invoice, SessionLocal, init_db

load_dotenv()
init_db()

ODOO_URL = os.getenv("ODOO_URL")
ODOO_DB = os.getenv("ODOO_DB")
ODOO_USERNAME = os.getenv("ODOO_USERNAME")
ODOO_PASSWORD = os.getenv("ODOO_PASSWORD")

if not all([ODOO_URL, ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD]):
    raise Exception("Missing Odoo credentials. Check your .env file.")


def get_odoo_models():
    common = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/common")
    uid = common.authenticate(ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD, {})
    if not uid:
        raise Exception("Authentication with Odoo failed.")
    models = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/object")
    return uid, models


def sync_contacts(db_session):
    uid, models = get_odoo_models()
    odoo_contacts = models.execute_kw(
        ODOO_DB,
        uid,
        ODOO_PASSWORD,
        "res.partner",
        "search_read",
        [[]],
        {"fields": ["id", "name", "email"]},
    )
    odoo_ids = [contact["id"] for contact in odoo_contacts]

    for rec in odoo_contacts:
        local_contact = db_session.query(Contact).filter_by(odoo_id=rec["id"]).first()
        if local_contact:
            local_contact.name = rec.get("name")
            local_contact.email = rec.get("email")
        else:
            new_contact = Contact(
                odoo_id=rec["id"], name=rec.get("name"), email=rec.get("email")
            )
            db_session.add(new_contact)

    db_session.query(Contact).filter(~Contact.odoo_id.in_(odoo_ids)).delete(
        synchronize_session=False
    )
    db_session.commit()
    print("Contacts synced.")


def sync_invoices(db_session):
    uid, models = get_odoo_models()
    odoo_invoices = models.execute_kw(
        ODOO_DB,
        uid,
        ODOO_PASSWORD,
        "account.move",
        "search_read",
        [[]],
        {"fields": ["id", "name", "amount_total"]},
    )
    odoo_ids = [inv["id"] for inv in odoo_invoices]

    for rec in odoo_invoices:
        local_inv = db_session.query(Invoice).filter_by(odoo_id=rec["id"]).first()
        if local_inv:
            local_inv.number = rec.get("name")
            local_inv.amount_total = rec.get("amount_total")
        else:
            new_inv = Invoice(
                odoo_id=rec["id"],
                number=rec.get("name"),
                amount_total=rec.get("amount_total"),
            )
            db_session.add(new_inv)

    db_session.query(Invoice).filter(~Invoice.odoo_id.in_(odoo_ids)).delete(
        synchronize_session=False
    )
    db_session.commit()
    print("Invoices synced.")


if __name__ == "__main__":
    db = SessionLocal()
    try:
        sync_contacts(db)
        sync_invoices(db)
    finally:
        db.close()
