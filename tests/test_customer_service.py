"""Pruebas de la lógica simulada de atención al cliente."""

from src.customer_service import (
    build_internal_context,
    contains_sensitive_information,
    extract_order_id,
    lookup_order,
)


def test_extract_order_id() -> None:
    """Debe reconocer identificadores PED-0000 sin importar mayúsculas."""

    assert extract_order_id("Revisa ped-1001 por favor") == "PED-1001"
    assert extract_order_id("No tengo número") is None


def test_lookup_order_prints_simulation_message(capsys) -> None:
    """La consulta de pedido debe evidenciar la simulación solicitada."""

    order = lookup_order("PED-1001")
    captured = capsys.readouterr()

    assert "Consultando base de datos de clientes..." in captured.out
    assert order is not None
    assert order["status"] == "En preparación"


def test_unknown_order_does_not_invent_information() -> None:
    """Un pedido inexistente debe generar instrucciones de no inventar."""

    context = build_internal_context("Busca el pedido PED-9999")

    assert "No existe información" in context
    assert "No inventes datos" in context


def test_detects_sensitive_information() -> None:
    """Debe detectar credenciales y no marcar consultas normales."""

    assert contains_sensitive_information(
        "Mi contraseña es secreta"
    ) is True

    assert contains_sensitive_information(
        "Quiero ver mi pedido"
    ) is False


def test_build_context_finds_matching_onigiri() -> None:
    """Una consulta específica debe recuperar el producto correcto."""

    context = build_internal_context(
        "¿Qué ingredientes tiene el Kinoko Teriyaki?"
    )

    assert "Kinoko Teriyaki" in context
    assert "mezcla de hongos en salsa teriyaki" in context
    assert '"price_mxn": 80' in context
    assert "PRODUCTOS FICTICIOS DISPONIBLES" in context


def test_build_context_lists_available_sauces() -> None:
    """Una consulta general de salsas debe recuperar las cuatro registradas."""

    context = build_internal_context("¿Qué salsas manejan?")

    assert "SALSAS DISPONIBLES" in context
    assert "Anguila" in context
    assert "Soya" in context
    assert "Aderezo Chipotle" in context
    assert "Sriracha" in context


def test_missing_order_id_requests_expected_format() -> None:
    """Una consulta de pedido incompleta debe solicitar un ID válido."""

    context = build_internal_context("¿Dónde está mi pedido?")

    assert "CONSULTA DE PEDIDO" in context
    assert "Falta un identificador" in context
    assert "PED-0000" in context


def test_unknown_business_question_requires_escalation() -> None:
    """Una política no documentada no debe convertirse en un dato inventado."""

    context = build_internal_context("¿Hacen entregas a Rosarito?")

    assert "No hay datos internos específicos" in context
    assert "no la inventes" in context
    assert "ofrece escalamiento" in context


def test_menu_query_contains_only_registered_catalog() -> None:
    """La consulta del menú debe recuperar los cinco productos registrados."""

    context = build_internal_context("¿Qué onigiris tienen?")

    expected_products = (
        "Spicy Tuna Mayo",
        "Salmon Queso Crema",
        "Chicken Teriyaki",
        "Kinoko Teriyaki",
        "Crispy Char Siu",
    )

    for product in expected_products:
        assert product in context

    assert "camarón" not in context.casefold()
    assert "camaron" not in context.casefold()


def test_human_agent_request_includes_escalation_instruction() -> None:
    """Una solicitud de atención humana debe recuperar la FAQ de escalamiento."""

    context = build_internal_context("Quiero hablar con una persona")

    assert "PREGUNTAS FRECUENTES APLICABLES" in context
    assert "FAQ-005" in context
    assert "¿Cómo contacto a un agente?" in context
    assert "escalamiento simulado" in context
    assert "no crea tickets reales ni conecta llamadas" in context