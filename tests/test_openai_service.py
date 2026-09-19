"""Pruebas del servicio LLM sin hacer llamadas reales a OpenAI."""

from types import SimpleNamespace

import pytest

import src.openai_service as openai_service_module
from src.config import Settings
from src.openai_service import LLMServiceError, OpenAIService


class FakeResponses:
    """Simula el recurso responses.create de OpenAI."""

    def __init__(self, output_text: str) -> None:
        self.output_text = output_text
        self.received_kwargs = None

    def create(self, **kwargs):
        self.received_kwargs = kwargs
        return SimpleNamespace(output_text=self.output_text)


class FakeClient:
    """Cliente que devuelve una respuesta controlada."""

    def __init__(self, output_text: str) -> None:
        self.responses = FakeResponses(output_text)


class RaisingResponses:
    """Simula responses.create lanzando una excepción."""

    def __init__(self, error: Exception) -> None:
        self.error = error

    def create(self, **kwargs):
        raise self.error


class RaisingClient:
    """Cliente falso utilizado para comprobar manejo de errores."""

    def __init__(self, error: Exception) -> None:
        self.responses = RaisingResponses(error)


def test_generate_reply_uses_responses_api() -> None:
    """El servicio debe usar el modelo configurado y Responses API."""

    client = FakeClient("Respuesta simulada")

    service = OpenAIService(
        settings=Settings("test-key", "test-model"),
        client=client,
    )

    result = service.generate_reply(
        history=[
            {
                "role": "user",
                "content": "Hola",
            }
        ],
        internal_context="Sin datos específicos.",
    )

    assert result == "Respuesta simulada"

    assert client.responses.received_kwargs["model"] == "test-model"

    assert (
        "CONVERSACIÓN"
        in client.responses.received_kwargs["input"]
    )


def test_generate_reply_rejects_empty_output() -> None:
    """Una respuesta sin texto debe convertirse en un error controlado."""

    service = OpenAIService(
        settings=Settings("test-key", "test-model"),
        client=FakeClient("   "),
    )

    with pytest.raises(
        LLMServiceError,
        match="no devolvió",
    ):
        service.generate_reply(
            history=[
                {
                    "role": "user",
                    "content": "Hola",
                }
            ],
            internal_context="Sin datos específicos.",
        )


def test_generate_reply_handles_authentication_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Una API key rechazada debe producir un error comprensible."""

    class FakeAuthenticationError(Exception):
        pass

    monkeypatch.setattr(
        openai_service_module.openai,
        "AuthenticationError",
        FakeAuthenticationError,
    )

    service = OpenAIService(
        settings=Settings("invalid-key", "test-model"),
        client=RaisingClient(
            FakeAuthenticationError("Invalid API key")
        ),
    )

    with pytest.raises(
        LLMServiceError,
        match="API key",
    ):
        service.generate_reply(
            history=[
                {
                    "role": "user",
                    "content": "Hola",
                }
            ],
            internal_context="Sin datos específicos.",
        )


def test_generate_reply_handles_rate_limit_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Un error de cuota debe convertirse en un error controlado."""

    class FakeRateLimitError(Exception):
        pass

    monkeypatch.setattr(
        openai_service_module.openai,
        "RateLimitError",
        FakeRateLimitError,
    )

    service = OpenAIService(
        settings=Settings("test-key", "test-model"),
        client=RaisingClient(
            FakeRateLimitError("insufficient_quota")
        ),
    )

    with pytest.raises(
        LLMServiceError,
        match="límite temporal de solicitudes o cuota",
    ):
        service.generate_reply(
            history=[
                {
                    "role": "user",
                    "content": "Hola",
                }
            ],
            internal_context="Sin datos específicos.",
        )