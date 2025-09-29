# streamlit_app.py
import os, time, requests
import streamlit as st

st.set_page_config(page_title="Cotidiana – Streamlit", page_icon="🤖", layout="centered")

API_BASE = os.getenv("API_BASE", "http://localhost:8080/api")

st.title("Cotidiana – Demo Streamlit")
st.caption("Consulta libre, respuesta sin límite de palabras e imagen alusiva por URL.")

with st.sidebar:
    st.header("Configuración")
    API_BASE = st.text_input("API_BASE", API_BASE, help="URL del backend FastAPI (ej: http://localhost:8080/api)")
    if st.button("Probar /health"):
        try:
            r = requests.get(f"{API_BASE}/health", timeout=10)
            st.success(r.json())
        except Exception as e:
            st.error(f"Error: {e}")

st.subheader("Haz tu consulta")
query = st.text_area("Escribe tu pregunta:", placeholder="Ej: Dame un plan de estudio para 3 días...")

c1, c2 = st.columns(2)
with c1:
    run = st.button("Enviar", type="primary")
with c2:
    clear = st.button("Limpiar")

if clear:
    st.experimental_rerun()

if run and query.strip():
    try:
        t0 = time.time()
        payload = {"query": query, "sessionId": None}
        resp = requests.post(f"{API_BASE}/chat", json=payload, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        dt = (time.time() - t0) * 1000

        st.markdown("### Respuesta")
        st.write(data.get("response", ""))

        st.markdown("### Imagen alusiva")
        img_url = data.get("image_url")
        if img_url: 
            st.image(img_url, caption=data.get("image_alt") or "Imagen alusiva", use_container_width=True)            
            st.write("**URL de la imagen:**")
            st.code(img_url, language="text")
        else:
            st.info("No se devolvió image_url desde el backend.")

        st.markdown("### Meta")
        st.json({
            "executionTime(ms_backend)": data.get("executionTime"),
            "flags": data.get("flags"),
            "timestamp": data.get("timestamp"),
            "latencia_total_ms_streamlit": dt,
        })

    except Exception as e:
        st.error(f"Error consultando API: {e}")
