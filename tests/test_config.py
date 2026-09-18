"""Pruebas de configuración."""

import pytest

from src.config import ConfigurationError, load_settings


def test_load_settings_success(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("OPENAI_MODEL", "test-model")

    settings = load_settings(env_file=None)

    assert settings.openai_api_key == "test-key"
    assert settings.openai_model == "test-model"


def test_load_settings_reports_missing_variables(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_MODEL", raising=False)

    with pytest.raises(ConfigurationError, match="OPENAI_API_KEY"):
        load_settings(env_file=None)
