"""Pruebas de la lógica simulada de atención al cliente."""

from src.customer_service import (
    build_internal_context,
    contains_sensitive_information,
    extract_order_id,
    lookup_order,
)


def test_extract_order_id() -> None:
    assert extract_order_id("Revisa ped-1001 por favor") == "PED-1001"
    assert extract_order_id("No tengo número") is None


def test_lookup_order_prints_simulation_message(capsys) -> None:
    order = lookup_order("PED-1001")
    captured = capsys.readouterr()

    assert "Consultando base de datos de clientes..." in captured.out
    assert order is not None
    assert order["status"] == "En preparación"


def test_unknown_order_does_not_invent_information() -> None:
    context = build_internal_context("Busca el pedido PED-9999")

    assert "No existe información" in context
    assert "No inventes datos" in context


def test_detects_sensitive_information() -> None:
    assert contains_sensitive_information(
        "Mi contraseña es secreta"
    ) is True

    assert contains_sensitive_information(
        "Quiero ver mi pedido"
    ) is False


def test_build_context_finds_matching_onigiri() -> None:
    context = build_internal_context(
        "¿Qué ingredientes tiene el Kinoko Teriyaki?"
    )

    assert "Kinoko Teriyaki" in context
    assert "mezcla de hongos en salsa teriyaki" in context
    assert '"price_mxn": 80' in context
    assert "PRODUCTOS FICTICIOS DISPONIBLES" in context


def test_build_context_lists_available_sauces() -> None:
    context = build_internal_context("¿Qué salsas manejan?")

    assert "SALSAS DISPONIBLES" in context
    assert "Anguila" in context
    assert "Soya" in context
    assert "Aderezo Chipotle" in context
    assert "Sriracha" in context
