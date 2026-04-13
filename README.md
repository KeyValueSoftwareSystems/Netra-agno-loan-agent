# Nova Loan Agent

An AI-powered loan agent application with a FastAPI backend and Next.js frontend.



## Getting Started

### 1. Create the `.env` file

Copy the example environment file and fill in your API keys:

```bash
cp .env.example .env
```

Open `.env` and update the following values:

| Variable               | Description                                      | Required |
|------------------------|--------------------------------------------------|----------|
| `NETRA_API_KEY`        | Your Netra API key                               | Yes      |
| `NETRA_OTLP_ENDPOINT`  | Netra telemetry endpoint                         | Yes      |
| `OPENAI_API_KEY`       | Your OpenAI API key (or use LiteLLM instead)     | Yes*     |
| `LITELLM_API_KEY`      | Your LiteLLM API key (alternative to OpenAI)     | Yes*     |

> \* Provide at least one of `OPENAI_API_KEY` or `LITELLM_API_KEY`.

### 2. Start the application

```bash
docker compose up -d
```

This starts two services in the background:

- **Backend** — FastAPI server on [http://localhost:8000](http://localhost:8000)
- **Frontend** — Next.js app on [http://localhost:3000](http://localhost:3000)

### 3. Verify the services are running

```bash
docker compose ps
```

### Stopping the application

```bash
docker compose down
```
