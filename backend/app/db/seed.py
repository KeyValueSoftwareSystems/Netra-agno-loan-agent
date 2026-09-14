import json
from sqlalchemy.orm import Session
from db.models import Customer, LoanProduct


SEED_PRODUCTS = [
    {
        "product_id": "FLEXI",
        "name": "FlexiLoan",
        "interest_rate_annual_pct": 11.5,
        "min_credit_score": 650,
        "max_amount": 500000,
        "available_tenures_months": json.dumps([12, 24, 36, 48, 60]),
        "processing_fee_pct": 1.5,
    },
    {
        "product_id": "PRIME",
        "name": "PrimeLoan",
        "interest_rate_annual_pct": 10.2,
        "min_credit_score": 750,
        "max_amount": 500000,
        "available_tenures_months": json.dumps([24, 36, 48]),
        "processing_fee_pct": 1.0,
    },
    {
        "product_id": "VALUE",
        "name": "ValueLoan",
        "interest_rate_annual_pct": 12.8,
        "min_credit_score": 600,
        "max_amount": 500000,
        "available_tenures_months": json.dumps([12, 24, 36]),
        "processing_fee_pct": 2.0,
    },
]


SEED_CUSTOMERS = [
    {
        "customer_id": "CUST-001",
        "verified": True,
        "full_name": "Priya Sharma",
        "kyc_status": "complete",
        "risk_flag": "none",
        "pan": "ABCDE1234G",
        "aadhaar": "234567891234",
        "phone": "9876543210",
        "credit_score": 780,
        "active_loans": json.dumps([]),
        "defaults_last_3_years": 0,
        "credit_utilization_pct": 22,
        "monthly_income": 95000,
        "employer": "Infosys Ltd",
        "employment_type": "salaried",
        "employment_tenure_months": 48,
        "existing_monthly_emi": 0,
        "average_bank_balance_6m": 285000,
        "internal_score": 92,
        "system_notes": "Clean profile, pre-approved for premium products",
    },
    {
        "customer_id": "CUST-002",
        "verified": True,
        "full_name": "Rahul Mehta",
        "kyc_status": "complete",
        "risk_flag": "none",
        "pan": "ABCPM5678Q",
        "aadhaar": "567890123456",
        "phone": "9823456789",
        "credit_score": 724,
        "active_loans": json.dumps([
            {"type": "car_loan", "outstanding": 380000, "monthly_emi": 12000}
        ]),
        "defaults_last_3_years": 0,
        "credit_utilization_pct": 34,
        "monthly_income": 85000,
        "employer": "TCS",
        "employment_type": "salaried",
        "employment_tenure_months": 36,
        "existing_monthly_emi": 12000,
        "average_bank_balance_6m": 145000,
        "internal_score": 78,
        "system_notes": "Existing car loan, good repayment history",
    },
    {
        "customer_id": "CUST-003",
        "verified": True,
        "full_name": "Arjun Paul",
        "kyc_status": "complete",
        "risk_flag": "medium",
        "pan": "ABCPP9012X",
        "aadhaar": "890123456789",
        "phone": "9712345678",
        "credit_score": 580,
        "active_loans": json.dumps([
            {"type": "personal_loan", "outstanding": 220000, "monthly_emi": 15000},
            {"type": "credit_card_debt", "outstanding": 95000, "monthly_emi": 13000},
        ]),
        "defaults_last_3_years": 1,
        "credit_utilization_pct": 78,
        "monthly_income": 65000,
        "employer": "Self — Reddy Consulting",
        "employment_type": "self_employed",
        "employment_tenure_months": 18,
        "existing_monthly_emi": 28000,
        "average_bank_balance_6m": 42000,
        "internal_score": 45,
        "system_notes": "High risk — low score, 1 default, high utilization",
    },
    {
        "customer_id": "CUST-004",
        "verified": True,
        "full_name": "Meera Iyer",
        "kyc_status": "complete",
        "risk_flag": "none",
        "pan": "ABCPI7890M",
        "aadhaar": "890123456780",
        "phone": "9712345670",
        "credit_score": 710,
        "active_loans": json.dumps([]),
        "defaults_last_3_years": 0,
        "credit_utilization_pct": 29,
        "monthly_income": 55000,
        "employer": "Wipro",
        "employment_type": "salaried",
        "employment_tenure_months": 14,
        "existing_monthly_emi": 0,
        "average_bank_balance_6m": 98000,
        "internal_score": 70,
        "system_notes": "Clean but low tenure, moderate income",
    },
]


def seed_database(session: Session) -> None:
    """Insert seed data if tables are empty."""
    if session.query(LoanProduct).count() == 0:
        for product_data in SEED_PRODUCTS:
            session.add(LoanProduct(**product_data))
        session.commit()

    if session.query(Customer).count() == 0:
        for customer_data in SEED_CUSTOMERS:
            session.add(Customer(**customer_data))
        session.commit()
