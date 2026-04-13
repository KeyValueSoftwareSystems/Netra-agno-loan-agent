from typing import TypedDict

class ActiveLoan(TypedDict):
    type: str
    outstanding: int
    monthly_emi: int

class CreditReport(TypedDict):
    credit_score: int
    active_loans: list[ActiveLoan]
    defaults_last_3_years: int
    credit_utilization_pct: int