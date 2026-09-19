"""Carga y validación de la configuración de FoodLabsAI."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


class ConfigurationError(RuntimeError):
    """Indica que faltan variables necesarias para ejecutar la aplicación."""


@dataclass(frozen=True)
class Settings:
    """Configuración validada de la aplicación."""

    openai_api_key: str
    openai_model: str


def load_settings(env_file: str | Path | None = ".env") -> Settings:
    """Carga el archivo .env y valida las variables obligatorias.

    Args:
        env_file: Ruta al archivo de variables. Usa ``None`` para omitirlo,
            algo útil durante pruebas automatizadas.

    Raises:
        ConfigurationError: Si falta la API key o el nombre del modelo.
    """

    if env_file is not None:
        load_dotenv(dotenv_path=env_file, override=False)

    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    model = os.getenv("OPENAI_MODEL", "").strip()

    missing: list[str] = []
    if not api_key:
        missing.append("OPENAI_API_KEY")
    if not model:
        missing.append("OPENAI_MODEL")

    if missing:
        variables = ", ".join(missing)
        raise ConfigurationError(
            f"Faltan variables de entorno obligatorias: {variables}. "
            "Copia .env.example como .env y completa sus valores."
        )

    return Settings(openai_api_key=api_key, openai_model=model)
