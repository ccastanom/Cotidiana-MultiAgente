import { useState, useRef, useEffect } from "react";
import type { ChatResponse as ChatResponseBase } from "../../types.index";

// Extendemos para tolerar los nuevos campos opcionales
type ChatResponse = ChatResponseBase & {
  // campos opcionales para UI enriquecida
  answer?: string;
  source?: string;
  image_prompt?: string;
  tts_text?: string;
  masked_query?: string;
  topic?: string | null; // tu tipo original permitía null
};

const topicIcons: Record<string, string> = {
  pasta: "/images/pasta.png",
  estudio: "/images/estudio.png",
  bicicleta: "/images/bicicleta.png",
  limpieza: "/images/limpieza.png",
  fuera_de_alcance: "/images/warning.png",
};

type Props = { data: ChatResponse };

export default function ResponseCard({ data }: Props) {
  const [speaking, setSpeaking] = useState(false);
  const utterRef = useRef<SpeechSynthesisUtterance | null>(null);

  const speak = () => {
    const text = data.tts_text ?? data.answer ?? data.response;
    if (!text) return;
    window.speechSynthesis.cancel();
    const u = new SpeechSynthesisUtterance(text);
    u.onstart = () => setSpeaking(true);
    u.onend = () => setSpeaking(false);
    utterRef.current = u;
    window.speechSynthesis.speak(u);
  };

  const stop = () => {
    window.speechSynthesis.cancel();
    setSpeaking(false);
  };

  useEffect(() => () => window.speechSynthesis.cancel(), []);

  // Elegimos qué mostrar:
  const showAnswer = data.answer ?? data.response; // fallback al campo viejo
  const topicKey =
    (data.topic && topicIcons[data.topic]) ? data.topic : "fuera_de_alcance";
  const imgSrc = topicIcons[topicKey];

  return (
    <div className="card">
      <div className="card__head">
        <b>Tema:</b> {data.topic ?? "—"} &nbsp;|&nbsp; <b>Fuente:</b> {data.source ?? "—"}
      </div>

      <p className="card__answer">{showAnswer}</p>

      <div className="card__media">
        <img className="card__img" src={imgSrc} alt={data.image_prompt ?? "Imagen sugerida"} />
        <small><b>Imagen sugerida:</b> {data.image_prompt ?? "—"}</small>
      </div>

      <div className="card__tts">
        {!speaking ? (
          <button onClick={speak}>🔊 Escuchar</button>
        ) : (
          <button onClick={stop}>⏹️ Detener</button>
        )}
      </div>

      <details className="card__meta">
        <summary>Meta</summary>
        <div><b>Query enmascarada:</b> {data.masked_query ?? "—"}</div>
      </details>
    </div>
  );
}

