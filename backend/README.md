# Nova Backend

FastAPI backend for the Nova Loan Agent, powered by [Agno](https://docs.agno.com/) and OpenAI GPT-4.1.

---

## Tech Stack

- **Agent Framework:** Agno SDK
- **LLM:** OpenAI GPT-4.1 (via `agno.models.openai.OpenAIChat`)
- **API:** FastAPI with uvicorn
- **Database:** SQLite (via SQLAlchemy for app data + Agno's `SqliteDb` for session storage)
- **Package Manager:** uv

---

## Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI entry point, /chat endpoint
│   ├── config.py            # Environment settings (Pydantic)
│   ├── logger.py            # Console + file logging setup
│   ├── agent/
│   │   ├── __init__.py      # Agno Agent definition + get_response()
│   │   ├── tools.py         # 7 plain Python tool functions
│   │   └── prompt.py        # System prompt for Nova
│   ├── db/
│   │   ├── __init__.py      # SQLite init, seed, query helpers
│   │   ├── models.py        # SQLAlchemy table definitions
│   │   └── seed.py          # Seed data (4 customers, 3 products)
│   └── schema/
│       └── chat_request.py  # Pydantic request model
├── Dockerfile
└── pyproject.toml
```

---

## API Endpoints

### `GET /`

Health check.

**Response:**
```json
{ "status": "ok", "agent": "Nova" }
```

### `POST /chat`

Main conversation endpoint.

**Request:**
```json
{
  "prompt": "I need a personal loan",
  "thread_id": "abc123",
  "files": [
    { "filename": "salary_slip.pdf", "mime_type": "application/pdf", "data": "" }
  ]
}
```

| Field      | Type            | Required | Description                                |
|------------|-----------------|----------|--------------------------------------------|
| `prompt`   | string          | Yes      | User message                               |
| `thread_id`| string or null  | No       | Session ID (auto-generated if not provided)|
| `files`    | array or null   | No       | Uploaded file metadata                     |

**Response:**
```json
{
  "response": "I've verified your identity. You are Priya Sharma...",
  "thread_id": "a1b2c3d4"
}
```

---

## Agent Tools

The agent has access to 7 tools that must be called in a specific order:

| # | Tool                      | Purpose                                        |
|---|---------------------------|------------------------------------------------|
| 1 | `verify_identity`         | Look up customer by PAN, Aadhaar, or phone     |
| 2 | `fetch_credit_report`     | Get credit score, loans, defaults              |
| 3 | `fetch_financial_profile` | Get income, employer, existing EMIs            |
| 4 | `search_loan_products`    | Find products matching the customer's score    |
| 5 | `check_eligibility`       | Evaluate DTI, score, amount, tenure            |
| 6 | `calculate_emi`           | Standard amortization EMI calculation          |
| 7 | `generate_pre_approval`   | Issue pre-approval with reference ID           |

---

## Database Schema

### `customers` table

| Column                    | Type    | Notes                           |
|---------------------------|---------|---------------------------------|
| `customer_id`             | TEXT PK | e.g. CUST-001                   |
| `full_name`               | TEXT    |                                 |
| `pan`                     | TEXT    | Unique                          |
| `aadhaar`                 | TEXT    | Unique                          |
| `phone`                   | TEXT    | Unique                          |
| `kyc_status`              | TEXT    | complete / pending              |
| `credit_score`            | INT     |                                 |
| `active_loans`            | TEXT    | JSON array                      |
| `defaults_last_3_years`   | INT     |                                 |
| `credit_utilization_pct`  | INT     |                                 |
| `monthly_income`          | INT     |                                 |
| `employer`                | TEXT    |                                 |
| `employment_type`         | TEXT    | salaried / self_employed        |
| `existing_monthly_emi`    | INT     |                                 |
| `average_bank_balance_6m` | INT     |                                 |
| `risk_flag`               | TEXT    | none / medium (internal only)   |
| `internal_score`          | INT     | Internal only                   |
| `system_notes`            | TEXT    | Internal only                   |

### `loan_products` table

| Column                     | Type    | Notes                          |
|----------------------------|---------|--------------------------------|
| `product_id`               | TEXT PK | FLEXI, PRIME, VALUE            |
| `name`                     | TEXT    | FlexiLoan, PrimeLoan, ValueLoan|
| `interest_rate_annual_pct` | REAL    | 10.2 – 12.8                   |
| `min_credit_score`         | INT     | 600 – 750                     |
| `max_amount`               | INT     | 500000                         |
| `available_tenures_months` | TEXT    | JSON array e.g. [12,24,36]    |
| `processing_fee_pct`       | REAL    |                                |

---

## Running Locally (without Docker)

```bash
cd backend

# Create virtual environment
uv venv --python 3.12
source .venv/bin/activate

# Install dependencies
uv sync

# Set environment
export OPENAI_API_KEY="sk-..."

# Run the server
cd app
python main.py
```

The server starts at http://localhost:8000. API docs at http://localhost:8000/docs.

---

## Environment Variables

| Variable         | Required | Default         | Description               |
|------------------|----------|-----------------|---------------------------|
| `OPENAI_API_KEY` | Yes      | —               | OpenAI API key            |
| `ENVIRONMENT`    | No       | `dev`           | `dev` enables hot reload  |
| `DATABASE_PATH`  | No       | `data/nova.db`  | Path to SQLite database   |
