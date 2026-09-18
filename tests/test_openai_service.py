"""Pruebas del servicio LLM sin hacer llamadas reales."""

from types import SimpleNamespace

import pytest

from src.config import Settings
from src.openai_service import LLMServiceError, OpenAIService


class FakeResponses:
    def __init__(self, output_text: str) -> None:
        self.output_text = output_text
        self.received_kwargs = None

    def create(self, **kwargs):
        self.received_kwargs = kwargs
        return SimpleNamespace(output_text=self.output_text)


class FakeClient:
    def __init__(self, output_text: str) -> None:
        self.responses = FakeResponses(output_text)


def test_generate_reply_uses_responses_api() -> None:
    client = FakeClient("Respuesta simulada")
    service = OpenAIService(
        settings=Settings("test-key", "test-model"),
        client=client,
    )

    result = service.generate_reply(
        history=[{"role": "user", "content": "Hola"}],
        internal_context="Sin datos específicos.",
    )

    assert result == "Respuesta simulada"
    assert client.responses.received_kwargs["model"] == "test-model"
    assert "CONVERSACIÓN" in client.responses.received_kwargs["input"]


def test_generate_reply_rejects_empty_output() -> None:
    service = OpenAIService(
        settings=Settings("test-key", "test-model"),
        client=FakeClient("   "),
    )

    with pytest.raises(LLMServiceError, match="no devolvió"):
        service.generate_reply(
            history=[{"role": "user", "content": "Hola"}],
            internal_context="Sin datos específicos.",
        )
