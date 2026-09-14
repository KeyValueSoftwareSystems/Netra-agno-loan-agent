import json
import logging
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from db.models import Base, Customer, LoanProduct
from db.seed import seed_database

_DB_PATH = os.environ.get("DATABASE_PATH", "data/nova.db")
_engine = None
_SessionLocal = None


def init_db() -> None:
    """Create tables and seed data. Called once at application startup."""
    global _engine, _SessionLocal

    os.makedirs(os.path.dirname(_DB_PATH) or ".", exist_ok=True)
    _engine = create_engine(f"sqlite:///{_DB_PATH}", echo=False)
    _SessionLocal = sessionmaker(bind=_engine)

    Base.metadata.create_all(_engine)
    logging.info(f"SQLite database initialised at {_DB_PATH}")

    with _SessionLocal() as session:
        seed_database(session)
        logging.info("Seed data loaded")


def get_session() -> Session:
    """Return a new SQLAlchemy session. Caller must close it."""
    if _SessionLocal is None:
        raise RuntimeError("Database not initialised — call init_db() first")
    return _SessionLocal()


# ---------------------------------------------------------------------------
# Query helpers used by agent tools
# ---------------------------------------------------------------------------

def get_customer_by_identifier(identifier_type: str, identifier_value: str) -> dict | None:
    """Look up a customer by PAN, AADHAAR, or PHONE. Returns a dict or None."""
    column_map = {"PAN": "pan", "AADHAAR": "aadhaar", "PHONE": "phone"}
    col_name = column_map.get(identifier_type.upper())
    if col_name is None:
        return None

    with get_session() as session:
        customer = session.query(Customer).filter(
            getattr(Customer, col_name) == identifier_value
        ).first()
        if customer is None:
            return None
        return _customer_to_dict(customer)


def get_customer_by_id(customer_id: str) -> dict | None:
    """Look up a customer by customer_id. Returns a dict or None."""
    with get_session() as session:
        customer = session.query(Customer).filter(
            Customer.customer_id == customer_id
        ).first()
        if customer is None:
            return None
        return _customer_to_dict(customer)


def get_credit_report(customer_id: str) -> dict | None:
    """Return the credit report portion of a customer record."""
    with get_session() as session:
        customer = session.query(Customer).filter(
            Customer.customer_id == customer_id
        ).first()
        if customer is None:
            return None
        return {
            "credit_score": customer.credit_score,
            "active_loans": json.loads(customer.active_loans or "[]"),
            "defaults_last_3_years": customer.defaults_last_3_years,
            "credit_utilization_pct": customer.credit_utilization_pct,
        }


def get_financial_profile(customer_id: str) -> dict | None:
    """Return the financial profile portion of a customer record."""
    with get_session() as session:
        customer = session.query(Customer).filter(
            Customer.customer_id == customer_id
        ).first()
        if customer is None:
            return None
        return {
            "monthly_income": customer.monthly_income,
            "employer": customer.employer,
            "employment_type": customer.employment_type,
            "employment_tenure_months": customer.employment_tenure_months,
            "existing_monthly_emi": customer.existing_monthly_emi,
            "average_bank_balance_6m": customer.average_bank_balance_6m,
        }


def search_products_by_score(credit_score: int) -> list[dict]:
    """Return all loan products the customer qualifies for based on credit score."""
    with get_session() as session:
        products = session.query(LoanProduct).filter(
            LoanProduct.min_credit_score <= credit_score
        ).all()
        return [_product_to_dict(p) for p in products]


def get_product_by_id(product_id: str) -> dict | None:
    """Look up a single loan product by product_id."""
    with get_session() as session:
        product = session.query(LoanProduct).filter(
            LoanProduct.product_id == product_id
        ).first()
        if product is None:
            return None
        return _product_to_dict(product)


def get_all_products() -> list[dict]:
    """Return every loan product (sorted by interest rate, lowest first)."""
    with get_session() as session:
        products = session.query(LoanProduct).order_by(
            LoanProduct.min_credit_score
        ).all()
        return [_product_to_dict(p) for p in products]


# ---------------------------------------------------------------------------
# Internal serialisation helpers
# ---------------------------------------------------------------------------

def _customer_to_dict(c: Customer) -> dict:
    return {
        "customer_id": c.customer_id,
        "verified": c.verified,
        "full_name": c.full_name,
        "kyc_status": c.kyc_status,
        "risk_flag": c.risk_flag,
        "pan": c.pan,
        "aadhaar": c.aadhaar,
        "phone": c.phone,
        "credit_score": c.credit_score,
        "active_loans": json.loads(c.active_loans or "[]"),
        "defaults_last_3_years": c.defaults_last_3_years,
        "credit_utilization_pct": c.credit_utilization_pct,
        "monthly_income": c.monthly_income,
        "employer": c.employer,
        "employment_type": c.employment_type,
        "employment_tenure_months": c.employment_tenure_months,
        "existing_monthly_emi": c.existing_monthly_emi,
        "average_bank_balance_6m": c.average_bank_balance_6m,
        "internal_score": c.internal_score,
        "system_notes": c.system_notes,
    }


def _product_to_dict(p: LoanProduct) -> dict:
    return {
        "product_id": p.product_id,
        "name": p.name,
        "interest_rate_annual_pct": p.interest_rate_annual_pct,
        "min_credit_score": p.min_credit_score,
        "max_amount": p.max_amount,
        "available_tenures_months": json.loads(p.available_tenures_months),
        "processing_fee_pct": p.processing_fee_pct,
    }
