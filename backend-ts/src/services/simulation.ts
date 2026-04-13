import { Netra, BaseTask, type TaskResult } from "netra-sdk";
import { getResponse } from "../agent/index.js";
import { randomUUID } from "node:crypto";

class LoanAgentTask extends BaseTask {
  async run(message: string, sessionId?: string | null): Promise<TaskResult> {
    const threadId = sessionId || randomUUID().replace(/-/g, "");

    Netra.setSessionId(threadId);

    let finalMessage: string;
    // Get response from the agent
    try {
      const response = await getResponse(message, threadId);
      finalMessage = response;
    } catch (e: any) {
      finalMessage = `Error: ${e.message}`;
    }

    return {
      message: finalMessage,
      sessionId: threadId,
    };
  }
}

export const runSimulation = async (datasetId: string) => {
  return await Netra.simulation.runSimulation({
    name: "Loan Agent Simulation",
    datasetId: datasetId,
    task: new LoanAgentTask(),
  });
};
