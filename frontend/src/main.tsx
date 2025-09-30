// frontend/src/main.tsx
import React from "react";
import { createRoot } from "react-dom/client";
import App from "../public/src/App";
import "../public/src/index.css";


createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
