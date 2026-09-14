from sqlalchemy import Column, String, Integer, Float, Boolean, Text, create_engine
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(String, primary_key=True)
    verified = Column(Boolean, default=True)
    full_name = Column(String, nullable=False)
    kyc_status = Column(String, default="complete")
    risk_flag = Column(String, default="none")
    pan = Column(String, unique=True, nullable=False)
    aadhaar = Column(String, unique=True, nullable=False)
    phone = Column(String, unique=True, nullable=False)

    # Credit report fields
    credit_score = Column(Integer, nullable=False)
    active_loans = Column(Text, default="[]")  # JSON string
    defaults_last_3_years = Column(Integer, default=0)
    credit_utilization_pct = Column(Integer, default=0)

    # Financial profile fields
    monthly_income = Column(Integer, nullable=False)
    employer = Column(String, nullable=False)
    employment_type = Column(String, nullable=False)
    employment_tenure_months = Column(Integer, default=0)
    existing_monthly_emi = Column(Integer, default=0)
    average_bank_balance_6m = Column(Integer, default=0)

    # Internal fields (never exposed to user)
    internal_score = Column(Integer, nullable=True)
    system_notes = Column(Text, nullable=True)


class LoanProduct(Base):
    __tablename__ = "loan_products"

    product_id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    interest_rate_annual_pct = Column(Float, nullable=False)
    min_credit_score = Column(Integer, nullable=False)
    max_amount = Column(Integer, nullable=False)
    available_tenures_months = Column(Text, nullable=False)  # JSON string e.g. "[12,24,36]"
    processing_fee_pct = Column(Float, nullable=False)
