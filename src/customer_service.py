"""Lógica local y simulada de atención al cliente."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
ORDER_PATTERN = re.compile(r"\bPED-\d{4}\b", re.IGNORECASE)

SENSITIVE_TERMS = (
    "contraseña",
    "password",
    "cvv",
    "nip",
    "número completo de tarjeta",
    "numero completo de tarjeta",
    "cuenta bancaria",
)


def _load_json(filename: str) -> dict[str, Any]:
    """Carga un archivo JSON ubicado en la carpeta data."""

    path = DATA_DIR / filename
    try:
        with path.open("r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError as exc:
        raise RuntimeError(f"No se encontró el archivo de datos: {path}") from exc
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"El archivo {path.name} contiene JSON inválido.") from exc


def extract_order_id(message: str) -> str | None:
    """Extrae un identificador de pedido con formato PED-0000."""

    match = ORDER_PATTERN.search(message)
    return match.group(0).upper() if match else None


def contains_sensitive_information(message: str) -> bool:
    """Detecta expresiones asociadas con credenciales o datos financieros."""

    normalized = message.casefold()
    return any(term in normalized for term in SENSITIVE_TERMS)


def lookup_order(order_id: str) -> dict[str, Any] | None:
    """Busca un pedido ficticio y muestra la evidencia de la simulación."""

    print("Consultando base de datos de clientes...")
    customers = _load_json("customers.json").get("customers", [])

    for customer in customers:
        for order in customer.get("orders", []):
            if order.get("order_id", "").upper() == order_id.upper():
                return {
                    "customer_id": customer.get("customer_id"),
                    "customer_name": customer.get("name"),
                    **order,
                }
    return None


def _relevant_faqs(message: str) -> list[dict[str, Any]]:
    normalized_words = set(re.findall(r"[a-záéíóúñü]+", message.casefold()))
    faqs = _load_json("faq.json").get("faqs", [])
    relevant: list[dict[str, Any]] = []

    for faq in faqs:
        keywords = {word.casefold() for word in faq.get("keywords", [])}
        if normalized_words & keywords:
            relevant.append(faq)

    return relevant[:3]


def _relevant_products(message: str) -> list[dict[str, Any]]:
    """Devuelve productos relacionados con una consulta del usuario."""

    normalized = message.casefold()
    catalog = _load_json("products.json").get("products", [])

    matched = [
        product
        for product in catalog
        if product.get("name", "").casefold() in normalized
        or any(
            keyword.casefold() in normalized
            for keyword in product.get("keywords", [])
        )
    ]

    if matched:
        return matched[:3]

    catalog_terms = (
        "recomienda",
        "recomiéndame",
        "recomiendame",
        "recomendar",
        "recomendación",
        "producto",
        "comprar",
        "busco",
        "necesito",
        "onigiri",
        "onigiris",
        "menú",
        "menu",
        "sabores",
        "ingredientes",
        "alérgenos",
        "alergenos",
        "precio",
        "precios",
        "cuesta",
        "cuestan",
    )

    if any(term in normalized for term in catalog_terms):
        return catalog[:5]

    return []


def _relevant_sauces(message: str) -> list[dict[str, Any]]:
    """Devuelve las salsas relacionadas o el catálogo cuando se consulta por salsas."""

    normalized = message.casefold()
    sauces = _load_json("sauces.json").get("sauces", [])

    matched = [
        sauce
        for sauce in sauces
        if sauce.get("name", "").casefold() in normalized
        or any(
            keyword.casefold() in normalized
            for keyword in sauce.get("keywords", [])
        )
    ]

    if matched:
        return matched

    sauce_terms = (
        "salsa",
        "salsas",
        "aderezo",
        "aderezos",
        "anguila",
        "soya",
        "chipotle",
        "sriracha",
        "siracha",
    )

    if any(term in normalized for term in sauce_terms):
        return sauces

    return []


def build_internal_context(message: str) -> str:
    """Construye contexto verificable para evitar respuestas inventadas."""

    context_parts: list[str] = []

    if contains_sensitive_information(message):
        context_parts.append(
            "SEGURIDAD: El usuario mencionó posibles credenciales o información "
            "financiera sensible. Indícale que no debe compartir esos datos."
        )

    order_id = extract_order_id(message)
    if order_id:
        order = lookup_order(order_id)
        if order:
            context_parts.append(
                "PEDIDO SIMULADO ENCONTRADO:\n"
                + json.dumps(order, ensure_ascii=False, indent=2)
            )
        else:
            context_parts.append(
                f"PEDIDO SIMULADO: No existe información para {order_id}. "
                "No inventes datos; ofrece verificar el identificador o escalar."
            )
    elif any(term in message.casefold() for term in ("pedido", "orden", "envío", "envio")):
        context_parts.append(
            "CONSULTA DE PEDIDO: Falta un identificador con formato PED-0000."
        )

    faqs = _relevant_faqs(message)
    if faqs:
        context_parts.append(
            "PREGUNTAS FRECUENTES APLICABLES:\n"
            + json.dumps(faqs, ensure_ascii=False, indent=2)
        )

    products = _relevant_products(message)
    if products:
        context_parts.append(
            "PRODUCTOS FICTICIOS DISPONIBLES:\n"
            + json.dumps(products, ensure_ascii=False, indent=2)
        )

    sauces = _relevant_sauces(message)
    if sauces:
        context_parts.append(
            "SALSAS DISPONIBLES:\n"
            + json.dumps(sauces, ensure_ascii=False, indent=2)
        )

    if not context_parts:
        context_parts.append(
            "No hay datos internos específicos para esta consulta. Si la respuesta "
            "requiere una política, pedido o acción no incluida, no la inventes y "
            "ofrece escalamiento."
        )

    return "\n\n".join(context_parts)
