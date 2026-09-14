# Nova Frontend

Next.js landing page for Meridian Bank with a floating AI chat widget that connects to the Nova backend.

---

## Tech Stack

- **Framework:** Next.js 16 (App Router, standalone output)
- **React:** 19
- **Styling:** Tailwind CSS v4, shadcn/ui (new-york style)
- **Icons:** lucide-react
- **Markdown:** react-markdown + remark-gfm (for rendering agent responses)

---

## Project Structure

```
frontend/
├── app/
│   ├── layout.tsx          # Root layout (dark mode, Geist fonts)
│   ├── page.tsx            # Meridian Bank landing page
│   └── globals.css         # Tailwind + shadcn theme tokens
├── components/
│   ├── ai/
│   │   └── askAI.tsx       # Chat widget (entire chat UI + API calls)
│   └── ui/                 # shadcn/ui primitives (Button, Dialog, etc.)
├── lib/
│   └── utils.ts            # cn() utility for class merging
├── public/                 # Static assets
├── Dockerfile
└── package.json
```

---

## How It Works

The frontend is a static Meridian Bank marketing page. The interactive part is the **chat widget** — a floating button in the bottom-right corner that opens a dialog.

### Chat Flow

1. User clicks the green chat button.
2. Types a message and presses Enter or Send.
3. Frontend sends `POST /chat` to the backend with `{ prompt, thread_id }`.
4. Backend returns `{ response, thread_id }`.
5. AI response is rendered as Markdown (tables, bold, links via GFM).
6. `thread_id` is stored in `localStorage` for session continuity.
7. Closing the chat clears the session and message history.

---

## Running Locally (without Docker)

```bash
cd frontend

# Install dependencies
npm install

# Set the backend URL (if not running on default port)
export NEXT_PUBLIC_API_URL=http://localhost:8000

# Start dev server
npm run dev
```

Open http://localhost:3000.

---

## Environment Variables

| Variable               | Required | Default                  | Description                |
|------------------------|----------|--------------------------|----------------------------|
| `NEXT_PUBLIC_API_URL`  | No       | `http://localhost:8000`  | Backend API base URL       |

This variable is read at build time for production builds and at runtime in development.

---

## Building for Production

```bash
npm run build
npm start
```

The Next.js standalone output is used in the Docker image for minimal container size.
