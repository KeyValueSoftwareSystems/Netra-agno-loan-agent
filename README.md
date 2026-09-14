# Nova — AI Personal Loan Assistant

Nova is an AI-powered conversational loan assistant for **Meridian Bank**. It guides customers through the personal loan journey — from identity verification to pre-approval — via a chat widget embedded on the bank's website.

Built with [Agno](https://docs.agno.com/) (agent framework), FastAPI (backend), and Next.js (frontend).

---

## Architecture

```
┌──────────────────────┐       POST /chat        ┌──────────────────────┐
│                      │ ───────────────────────► │                      │
│   Next.js Frontend   │                          │   FastAPI Backend    │
│   (port 3000)        │ ◄─────────────────────── │   (port 8000)        │
│                      │    { response, thread_id }│                      │
└──────────────────────┘                          └──────────┬───────────┘
                                                             │
                                                    ┌────────▼────────┐
                                                    │   Agno Agent    │
                                                    │   (Nova)        │
                                                    │                 │
                                                    │  7 tools        │
                                                    │  GPT-4.1        │
                                                    │  SQLite storage │
                                                    └────────┬────────┘
                                                             │
                                                    ┌────────▼────────┐
                                                    │   SQLite DB     │
                                                    │   (nova.db)     │
                                                    │                 │
                                                    │  customers      │
                                                    │  loan_products  │
                                                    │  agent sessions │
                                                    └─────────────────┘
```

---

## Quick Start

### 1. Set up environment

```bash
cp .env.example .env
```

Open `.env` and paste your OpenAI API key:

```
OPENAI_API_KEY=sk-...
```

### 2. Start everything

```bash
docker compose up --build
```

This starts two services:

| Service    | URL                          | Description                    |
|------------|------------------------------|--------------------------------|
| Backend    | http://localhost:8000        | FastAPI + Agno agent           |
| Frontend   | http://localhost:3000        | Meridian Bank website + chat   |

### 3. Open the app

Go to **http://localhost:3000** and click the green chat button in the bottom-right corner.

---

## How to Use the Agent

Nova follows a structured loan application flow. Here's a walkthrough:

### Step 1 — Verify Identity

Start by providing a PAN, Aadhaar, or phone number. The agent must verify your identity before anything else.

> "Hi, I'd like to check my loan eligibility. My PAN is ABCDE1234G."

### Step 2 — Agent Fetches Your Profile

After verification, Nova automatically retrieves your credit report and financial profile (this happens behind the scenes).

### Step 3 — State Your Loan Requirement

Tell the agent how much you want to borrow and for how long.

> "I need a loan of 3 lakhs for 2 years."

### Step 4 — View Matching Products

The agent searches for loan products you qualify for and shows them in a table with interest rates, tenures, and fees.

### Step 5 — Check Eligibility

Nova runs an eligibility check against the selected product and tells you whether you qualify (or the specific reasons you don't).

### Step 6 — Pre-Approval

If eligible, the agent generates a pre-approval with a reference ID, validity date, and next steps — including a mandatory disclaimer.

---

## Test Customer Data

The database comes pre-loaded with four test customers. Use any of these identifiers to get started:

| Name           | PAN         | Aadhaar        | Phone        | Credit Score | Monthly Income | Notes                        |
|----------------|-------------|----------------|--------------|--------------|----------------|------------------------------|
| Priya Sharma   | ABCDE1234G  | 234567891234   | 9876543210   | 780          | 95,000         | Clean profile, high score    |
| Rahul Mehta    | ABCPM5678Q  | 567890123456   | 9823456789   | 724          | 85,000         | Has car loan (12K EMI)       |
| Arjun Paul     | ABCPP9012X  | 890123456789   | 9712345678   | 580          | 65,000         | Low score, 1 default, risky  |
| Meera Iyer     | ABCPI7890M  | 890123456780   | 9712345670   | 710          | 55,000         | Clean but moderate income    |

### Available Loan Products

| Product     | Interest Rate | Min Credit Score | Max Amount   | Tenures (months)   |
|-------------|---------------|------------------|--------------|---------------------|
| FlexiLoan   | 11.5%         | 650              | 5,00,000     | 12, 24, 36, 48, 60 |
| PrimeLoan   | 10.2%         | 750              | 5,00,000     | 24, 36, 48          |
| ValueLoan   | 12.8%         | 600              | 5,00,000     | 12, 24, 36          |

---

## Stopping the Application

```bash
docker compose down
```

To also remove the persisted database volume:

```bash
docker compose down -v
```

---

## Project Structure

```
netra-ai-loan-agent/
├── backend/                 # FastAPI + Agno agent (Python)
├── frontend/                # Next.js landing page + chat widget
├── docker-compose.yml       # Runs both services
├── .env.example             # Environment template
├── PRD.md                   # Product requirements document
├── NETRA_INTEGRATION.md     # Reference for re-adding Netra observability
└── README.md                # This file
```

See [backend/README.md](backend/README.md) and [frontend/README.md](frontend/README.md) for service-specific docs.

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Agent Framework | [Agno](https://docs.agno.com/) |
| LLM | OpenAI GPT-4.1 |
| Backend | Python 3.12, FastAPI, SQLAlchemy |
| Database | SQLite |
| Frontend | Next.js 16, React 19, Tailwind CSS, shadcn/ui |
| Container | Docker Compose |
