from typing import TypedDict
from schema.credit_report import CreditReport
from schema.financial_profile import FinancialProfile
from schema.eligibility import Eligibility

class Customer(TypedDict):
    customer_id: str
    verified: bool
    full_name: str
    kyc_status: str
    risk_flag: str
    credit_report: CreditReport
    financial_profile: FinancialProfile
    pan: str
    aadhar: str
    phone: str
    eligibility: Eligibility