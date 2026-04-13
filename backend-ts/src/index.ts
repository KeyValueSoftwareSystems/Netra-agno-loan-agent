import { serve } from "@hono/node-server";
import { Hono } from "hono";
import { cors } from "hono/cors";
import { Netra, NetraInstruments } from "netra-sdk";
import { randomUUID } from "node:crypto";
import { getResponse } from "./agent/index.js";
import type { ChatRequest } from "./schema/chat-request.js";
import { initDb } from "./db/index.js";
import { runSimulation } from "./services/simulation.js";
import { runEvaluation } from "./services/evaluation.js";

await Netra.init({
  appName: "Nova Agent TS",
  headers: `x-api-key=${process.env.NETRA_API_KEY}`,
  debugMode: true,
  environment: process.env.ENVIRONMENT || "dev",
  blockInstruments: new Set([
    NetraInstruments.LANGCHAIN,
    NetraInstruments.LANGGRAPH,
    NetraInstruments.OPENAI,
    NetraInstruments.GROQ,
    NetraInstruments.HTTP,
    NetraInstruments.HTTPS,
    NetraInstruments.FETCH,
  ]),
});

process.on("SIGTERM", async () => {
  await Netra.shutdown();
  process.exit(0);
});

process.on("SIGINT", async () => {
  await Netra.shutdown();
  process.exit(0);
});

const app = new Hono();
initDb();
app.use(
  "*",
  cors({
    origin: ["http://localhost:3000", "http://127.0.0.1:3000"],
    allowMethods: ["POST", "GET", "OPTIONS"],
    allowHeaders: ["Content-Type", "Authorization"],
    credentials: true,
    maxAge: 600,
  }),
);

app.options("*", (c) => c.text("", 200));

app.post("/chat", async (c) => {
  try {
    const body = await c.req.json<ChatRequest>();

    const existingThreadId =
      body.thread_id && body.thread_id.trim().length > 0
        ? body.thread_id
        : null;

    const threadId = (existingThreadId ?? randomUUID()).replace(/-/g, "");

    Netra.setSessionId(threadId);

    const responseText = await getResponse(body.prompt, threadId);

    return c.json({
      response: responseText,
      thread_id: threadId,
    });
  } catch (err) {
    console.error(err);
    return c.json({ error: "An error occurred" }, 500);
  }
});

app.post("/simulation/:dataset_id", async (c) => {
  try {
    const datasetId = c.req.param("dataset_id");
    const result = await runSimulation(datasetId);
    if (!result) {
      throw new Error("Simulation failed");
    }
    return c.json(result);
  } catch (err: any) {
    console.error(err);
    return c.json({ error: err.message || "An error occurred" }, 500);
  }
});

app.post("/single-turn/:dataset_id", async (c) => {
  try {
    const datasetId = c.req.param("dataset_id");
    const result = await runEvaluation(datasetId);
    if (!result) {
      throw new Error("Evaluation failed");
    }
    return c.json(result);
  } catch (err: any) {
    console.error(err);
    return c.json({ error: err.message || "An error occurred" }, 500);
  }
});

serve(
  {
    fetch: app.fetch,
    port: 8000,
  },
  (info) => {
    console.log(`Server is running on http://localhost:${info.port}`);
  },
);
