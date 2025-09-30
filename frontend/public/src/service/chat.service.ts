import axios from "axios";
import type { ChatResponse } from "../types.index";


const API_BASE_URL: string =
  ( (import.meta as any).env?.VITE_API_URL as string ) ?? "http://localhost:8080/api";

  const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: { "Content-Type": "application/json" },
});

export async function sendMessage(query: string, sessionId?: string): Promise<ChatResponse> {
  const payload = { query, sessionId };
  const resp = await api.post<ChatResponse>("/chat", payload);
  return resp.data;
}

export async function getLogs() {
  const resp = await api.get("/logs");
  return resp.data;
}

export async function healthCheck() {
  const resp = await api.get("/health");
  return resp.data;
}
