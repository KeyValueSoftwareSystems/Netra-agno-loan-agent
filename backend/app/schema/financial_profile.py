from typing import TypedDict

class FinancialProfile(TypedDict):
    monthly_income: int
    employer: str
    employment_type: str
    employment_tenure_months: int
    existing_monthly_emi: int
    average_bank_balance_6m: int