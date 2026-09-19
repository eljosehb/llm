"""Integración aislada con la Responses API de OpenAI."""

from __future__ import annotations

from typing import Any

import openai
from openai import OpenAI

from src.config import Settings
from src.prompts import SYSTEM_PROMPT


class LLMServiceError(RuntimeError):
    """Error controlado al generar una respuesta con el modelo."""


class OpenAIService:
    """Genera respuestas del chatbot mediante la Responses API."""

    def __init__(self, settings: Settings, client: Any | None = None) -> None:
        self.settings = settings
        self.client = client or OpenAI(
            api_key=settings.openai_api_key,
            timeout=30.0,
            max_retries=2,
        )

    @staticmethod
    def _format_conversation(history: list[dict[str, str]]) -> str:
        """Convierte el historial reciente en un texto fácil de auditar."""

        role_names = {"user": "Cliente", "assistant": "FoodLabsAI"}
        recent_history = history[-12:]
        lines = [
            f"{role_names.get(message['role'], message['role'])}: "
            f"{message['content']}"
            for message in recent_history
        ]
        return "\n".join(lines)

    def generate_reply(
        self,
        history: list[dict[str, str]],
        internal_context: str,
    ) -> str:
        """Solicita una respuesta al modelo y traduce errores técnicos."""

        conversation = self._format_conversation(history)
        model_input = (
            "CONVERSACIÓN:\n"
            f"{conversation}\n\n"
            "CONTEXTO INTERNO PROPORCIONADO POR LA APLICACIÓN:\n"
            f"{internal_context}\n\n"
            "Responde al último mensaje del cliente."
        )

        try:
            response = self.client.responses.create(
                model=self.settings.openai_model,
                instructions=SYSTEM_PROMPT,
                input=model_input,
            )
        except openai.AuthenticationError as exc:
            raise LLMServiceError(
                "La API key no es válida o no tiene autorización."
            ) from exc
        except openai.RateLimitError as exc:
            raise LLMServiceError(
                "La API alcanzó su límite temporal de solicitudes o cuota."
            ) from exc
        except openai.APITimeoutError as exc:
            raise LLMServiceError(
                "La solicitud tardó demasiado. Intenta nuevamente."
            ) from exc
        except openai.APIConnectionError as exc:
            raise LLMServiceError(
                "No fue posible conectarse con OpenAI. Verifica tu conexión."
            ) from exc
        except openai.APIStatusError as exc:
            raise LLMServiceError(
                f"OpenAI devolvió un error HTTP {exc.status_code}."
            ) from exc
        except openai.APIError as exc:
            raise LLMServiceError(
                "Ocurrió un error inesperado al comunicarse con OpenAI."
            ) from exc

        output_text = getattr(response, "output_text", "")
        if not output_text or not output_text.strip():
            raise LLMServiceError("El modelo no devolvió una respuesta de texto.")

        return output_text.strip()
