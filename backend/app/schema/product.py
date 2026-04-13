from typing import TypedDict

class Product(TypedDict):
    product_id: str
    name: str
    interest_rate_annual_pct: float
    min_credit_score: int
    available_tenures_months: list[int]
    processing_fee_pct: float
    max_amount: int