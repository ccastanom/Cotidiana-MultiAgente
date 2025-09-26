export interface ChatResponse {
  response: string;
  topic: string | null;
  executionTime: number;
  flags: {
    blocked: boolean;
    offtopic: boolean;
    pii_in: boolean;
    no_data: boolean;
  };
  timestamp: number;
}
