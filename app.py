"""Interfaz web principal de FoodLabsAI para OnigiriDanshi."""

from __future__ import annotations

import streamlit as st

from src.config import ConfigurationError, Settings, load_settings
from src.customer_service import build_internal_context
from src.openai_service import LLMServiceError, OpenAIService

WELCOME_MESSAGE = (
    "¡Irasshaimase! Soy FoodLabsAI, el asistente virtual de OnigiriDanshi. "
    "Puedo ayudarte con nuestro menú de onigiris, ingredientes y consultas "
    "simuladas de pedidos. ¿En qué puedo ayudarte hoy?"
)


@st.cache_resource
def create_service(settings: Settings) -> OpenAIService:
    """Crea una sola instancia reutilizable del cliente de OpenAI."""

    return OpenAIService(settings)


st.set_page_config(
    page_title="FoodLabsAI | OnigiriDanshi",
    page_icon="🍙",
    layout="centered",
)

st.title("🍙 FoodLabsAI")
st.caption(
    "Asistente virtual de OnigiriDanshi · Proyecto académico. "
    "Las consultas de pedidos son simuladas y no ejecutan operaciones reales."
)

try:
    app_settings = load_settings()
except ConfigurationError as error:
    st.error(str(error))
    st.code(
        "cp .env.example .env  # Linux/WSL\n"
        "Copy-Item .env.example .env  # PowerShell",
        language="powershell",
    )
    st.stop()

service = create_service(app_settings)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": WELCOME_MESSAGE}
    ]

with st.sidebar:
    st.subheader("Pruebas sugeridas")
    st.markdown(
        "- ¿Qué sabores de onigiri tienen?\n"
        "- ¿Qué ingredientes tiene el Spicy Tuna Mayo?\n"
        "- ¿Qué contiene el Kinoko Teriyaki?\n"
        "- ¿Qué salsas manejan?\n"
        "- ¿Cuál es el estado del pedido PED-1001?\n"
        "- Tengo una alergia, ¿qué información tienen?\n"
        "- Quiero hablar con una persona."
    )

    if st.button("Limpiar conversación", use_container_width=True):
        st.session_state.messages = [
            {"role": "assistant", "content": WELCOME_MESSAGE}
        ]
        st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_message := st.chat_input(
    "Escribe tu consulta sobre OnigiriDanshi, ingredientes o pedidos"
):
    clean_message = user_message.strip()

    if not clean_message:
        st.warning("Escribe una consulta antes de enviarla.")
        st.stop()

    st.session_state.messages.append(
        {"role": "user", "content": clean_message}
    )

    with st.chat_message("user"):
        st.markdown(clean_message)

    try:
        internal_context = build_internal_context(clean_message)

        with st.chat_message("assistant"):
            with st.spinner("Analizando la consulta..."):
                assistant_reply = service.generate_reply(
                    history=st.session_state.messages,
                    internal_context=internal_context,
                )

            st.markdown(assistant_reply)

    except (LLMServiceError, RuntimeError) as error:
        assistant_reply = (
            "No pude procesar la consulta en este momento. "
            f"Detalle: {error}"
        )

        with st.chat_message("assistant"):
            st.error(assistant_reply)

    st.session_state.messages.append(
        {"role": "assistant", "content": assistant_reply}
    )
