# FoodLabsAI

FoodLabsAI es un proyecto académico de atención al cliente automatizada construido con Python, Streamlit y la Responses API de OpenAI. En esta demostración, FoodLabsAI funciona como asistente virtual de **OnigiriDanshi**, una marca de comida japonesa especializada en onigiris.

La aplicación utiliza datos ficticios y no se conecta a una base de datos real. Cuando se consulta un pedido, ejecuta la simulación solicitada por la actividad:

```python
print("Consultando base de datos de clientes...")
```

## 1. Objetivo del proyecto

Demostrar el uso práctico de un modelo de lenguaje de gran escala en un escenario de atención al cliente. FoodLabsAI combina un LLM con datos locales en JSON para responder preguntas sobre el menú de OnigiriDanshi, ingredientes, alérgenos documentados y pedidos simulados.

## 2. Funcionalidades

- Chat web con historial durante la sesión.
- Respuestas generadas mediante OpenAI Responses API.
- Menú de cinco onigiris almacenado en JSON.
- Consultas sobre ingredientes y alérgenos documentados.
- Recomendaciones sencillas basadas en palabras clave.
- Consulta simulada de pedidos con identificadores `PED-0000`.
- Preguntas frecuentes cargadas desde JSON.
- Advertencias ante solicitudes de información sensible.
- Escalamiento verbal cuando la información no está disponible.
- Manejo de errores de configuración y de la API.
- Pruebas unitarias que no consumen créditos de OpenAI.

## 3. Menú de demostración de OnigiriDanshi

| Producto | Ingredientes cargados | Precio |
|---|---|---:|
| Spicy Tuna Mayo | Medallón de atún, mayonesa spicy | $80 MXN |
| Salmon Queso Crema | Salmón a la plancha, queso crema, soya | $80 MXN |
| Chicken Teriyaki | Pechuga de pollo en salsa teriyaki | $80 MXN |
| Kinoko Teriyaki | Mezcla de hongos en salsa teriyaki | $80 MXN |
| Crispy Char Siu | Carne molida de cerdo frita en salsa char siu | $80 MXN |

Todos los onigiris del catálogo tienen un precio de **$80 MXN**.

### Salsas disponibles

- Anguila
- Soya
- Aderezo Chipotle
- Sriracha

La composición interna de estas salsas no está documentada en esta versión. Por ello, FoodLabsAI no debe inventar sus ingredientes ni alérgenos, ni garantizar que un producto sea seguro para una persona con alergias.

## 4. Tecnologías utilizadas

- Python 3.10 o posterior.
- OpenAI Python SDK.
- Responses API.
- Streamlit.
- python-dotenv.
- JSON.
- Pytest.
- Git y GitHub.

## 5. Estructura del proyecto

```text
FoodLabsAI/
├── app.py
├── data/
│   ├── customers.json
│   ├── faq.json
│   ├── products.json
│   └── sauces.json
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── customer_service.py
│   ├── openai_service.py
│   └── prompts.py
├── tests/
│   ├── test_config.py
│   ├── test_customer_service.py
│   └── test_openai_service.py
├── .env.example
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md
```

## 6. Requisitos previos

Necesitas:

- Python 3.10 o posterior.
- Git.
- Una API key válida de OpenAI.
- Un modelo disponible para el proyecto de OpenAI.
- Cuota o facturación de API disponible.

## 7. Crear y activar el entorno virtual

### Linux o WSL

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Si PowerShell bloquea la activación:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## 8. Instalar dependencias

Desde la carpeta raíz del proyecto:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 9. Configurar variables de entorno

### Linux o WSL

```bash
cp .env.example .env
```

### Windows PowerShell

```powershell
Copy-Item .env.example .env
```

Edita `.env`:

```env
OPENAI_API_KEY=tu_api_key_real
OPENAI_MODEL=un_modelo_disponible_en_tu_cuenta
```

Nunca subas `.env` a GitHub.

## 10. Ejecutar la aplicación

Desde la raíz:

```bash
python -m streamlit run app.py
```

Streamlit mostrará una dirección local, normalmente `http://localhost:8501`.

## 11. Uso de la interfaz

FoodLabsAI recibe preguntas escritas en lenguaje natural. El asistente usa los archivos JSON como fuente local de verdad antes de generar una respuesta mediante el LLM.

Ejemplos:

- `¿Qué sabores de onigiri tienen?`
- `¿Qué ingredientes tiene el Spicy Tuna Mayo?`
- `¿Qué contiene el Kinoko Teriyaki?`
- `¿Cuánto cuestan los onigiris?`
- `¿Qué salsas manejan?`
- `¿El Salmon Queso Crema contiene soya?`
- `¿Cuál es el estado del pedido PED-1001?`
- `Quiero hablar con una persona.`

## 12. Consulta simulada de pedidos

Los pedidos se encuentran en `data/customers.json`.

Ejemplo:

```text
¿Cuál es el estado del pedido PED-1001?
```

La terminal debe mostrar:

```text
Consultando base de datos de clientes...
```

La aplicación no consulta ni modifica una base de datos real.

## 13. Ejecutar pruebas

Las pruebas automatizadas utilizan datos locales y clientes simulados para evitar consumo de API.

```bash
pytest
```

También puedes usar:

```bash
python -m pytest
```

Resultado esperado para esta versión:

```text
10 passed
```

## 14. Errores comunes

### `ModuleNotFoundError: No module named 'dotenv'`

Verifica que el entorno virtual esté activo e instala las dependencias:

```bash
python -m pip install -r requirements.txt
```

### Faltan variables de entorno

Comprueba que `.env` esté en la raíz y contenga `OPENAI_API_KEY` y `OPENAI_MODEL`.

### API key inválida

Revisa la clave del proyecto de OpenAI y evita espacios adicionales.

### Error `429 insufficient_quota`

La API key fue detectada, pero el proyecto no tiene cuota disponible. Revisa Usage y Billing en OpenAI Platform.

### Modelo no disponible

Cambia `OPENAI_MODEL` por un modelo al que tu proyecto tenga acceso.

### Streamlit sigue mostrando información anterior

Detén la aplicación con `Ctrl + C`, vuelve a ejecutarla y usa el botón **Limpiar conversación**.

## 15. Seguridad

- La API key se almacena únicamente en `.env`.
- `.env` está incluido en `.gitignore`.
- Los clientes y pedidos son ficticios.
- FoodLabsAI no solicita contraseñas, CVV, NIP ni números completos de tarjeta.
- Todos los onigiris del catálogo están registrados en $80 MXN.
- El asistente no inventa ingredientes, alérgenos ni políticas.
- Las salsas disponibles son Anguila, Soya, Aderezo Chipotle y Sriracha.
- Si la composición interna de una salsa no está documentada, debe indicarlo.
- Ante una alergia, no garantiza que un producto sea seguro ni ausencia de contaminación cruzada.
- La aplicación no ejecuta reembolsos, cancelaciones, cambios ni tickets reales.

## 16. Limitaciones conocidas

- No existe una base de datos persistente.
- El historial se conserva únicamente durante la sesión de Streamlit.
- La búsqueda local utiliza reglas y palabras clave sencillas.
- Todos los onigiris comparten un precio fijo de $80 MXN.
- No está documentada la composición interna de las salsas disponibles.
- El escalamiento a una persona es informativo y simulado.
- La aplicación no verifica inventario ni disponibilidad real.

## 17. Control de versiones sugerido

```bash
git status
git add .
git commit -m "feat: rebrand app as FoodLabsAI for OnigiriDanshi"
```
