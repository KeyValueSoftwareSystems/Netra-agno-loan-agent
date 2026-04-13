from typing import TypedDict

class Eligibility(TypedDict):
    eligible: bool
    max_approved_amount: int
    requested_amount: int
    debt_to_income_ratio: float
    rejection_reasons: list[str]
    policy_version: str