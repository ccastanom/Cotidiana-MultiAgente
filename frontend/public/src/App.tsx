import React, { useState } from "react";
import { sendMessage, getLogs } from "./service/chat.service";


export default function App() {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState<string[]>([
    "¡Hola! Soy Cotidiana: puedo ayudar con cocinar pasta, técnicas de estudio, uso seguro de bicicleta y limpieza del hogar."
  ]);
  const [logs, setLogs] = useState<any[]>([]);

  const onSend = async () => {
    if (!query.trim()) return;
    setMessages(prev => [...prev, `Tú: ${query}`]);
    try {
      const res = await sendMessage(query);
      setMessages(prev => [...prev, `Cotidiana: ${res.response}`]);
    } catch (e) {
      setMessages(prev => [...prev, "Error de conexión con el backend."]);
    }
    setQuery("");
  };

  const loadLogs = async () => {
    const l = await getLogs();
    setLogs(l);
  };

  return (
    <div style={{ maxWidth: 900, margin: "2rem auto", padding: 20, background: "#fff", borderRadius: 8 }}>
      <h1>Cotidiana</h1>
      <div style={{ display: "flex", gap: 8, marginBottom: 12 }}>
        <input style={{ flex: 1, padding: 8 }} value={query} onChange={e => setQuery(e.target.value)} placeholder="Haz una pregunta..." />
        <button onClick={onSend}>Enviar</button>
        <button onClick={loadLogs}>Cargar logs</button>
      </div>
      <div style={{ minHeight: 200, border: "1px solid #eee", padding: 12 }}>
        {messages.map((m, i) => <div key={i} style={{ marginBottom: 8 }}>{m}</div>)}
      </div>
      <hr style={{ margin: "16px 0" }} />
      <div>
        <h3>Logs (últimos)</h3>
        {logs.map((l: any, i: number) => (
          <div key={i} style={{ fontSize: 12, marginBottom: 6 }}>
            [{new Date(l.timestamp).toLocaleString()}] {l.query} | {JSON.stringify(l.flags)} | {l.ms}ms
          </div>
        ))}
      </div>
    </div>
  );
}
