import os
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./local_data.db")

engine = sa.create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class Contact(Base):
    __tablename__ = "contacts"
    id = sa.Column(sa.Integer, primary_key=True, index=True)
    odoo_id = sa.Column(sa.Integer, unique=True, index=True)
    name = sa.Column(sa.String)
    email = sa.Column(sa.String)


class Invoice(Base):
    __tablename__ = "invoices"
    id = sa.Column(sa.Integer, primary_key=True, index=True)
    odoo_id = sa.Column(sa.Integer, unique=True, index=True)
    number = sa.Column(sa.String)
    amount_total = sa.Column(sa.Float)


def init_db():
    Base.metadata.create_all(bind=engine)
