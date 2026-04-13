export interface ChatRequest {
  prompt: string;
  /**
   * Optional thread identifier coming from the client.
   * When omitted or null, the server will generate one.
   */
  thread_id?: string | null;
}
