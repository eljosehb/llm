# FoodLabsAI

FoodLabsAI es un proyecto académico de atención al cliente automatizada construido con Python, Streamlit y la Responses API de OpenAI. En esta demostración, FoodLabsAI funciona como asistente virtual de **OnigiriDanshi**, una marca de comida japonesa especializada en onigiris.

La aplicación combina un modelo de lenguaje de gran escala (LLM) con datos locales en JSON para responder preguntas sobre productos, ingredientes, precios, salsas, preguntas frecuentes y pedidos simulados. No se conecta a una base de datos real.

Cuando se consulta un pedido, la aplicación ejecuta la simulación solicitada por la actividad:

```python
print("Consultando base de datos de clientes...")
```

---

## 1. Objetivo del proyecto

El objetivo de FoodLabsAI es demostrar el uso práctico de un LLM en un escenario realista de atención al cliente mediante la API de OpenAI.

El proyecto busca demostrar que un asistente puede:

- comprender preguntas escritas en lenguaje natural;
- responder preguntas frecuentes;
- recomendar productos usando información del negocio;
- consultar pedidos ficticios;
- mantener el contexto durante una conversación;
- reconocer cuándo no dispone de información suficiente;
- evitar inventar datos del negocio;
- proteger información sensible;
- ofrecer escalamiento a atención humana cuando corresponde.

---

## 2. Funcionalidades

FoodLabsAI incluye:

- interfaz web de chat creada con Streamlit;
- integración con OpenAI mediante la Responses API;
- historial conversacional durante la sesión;
- catálogo de OnigiriDanshi almacenado en JSON;
- consultas sobre productos, ingredientes y precios;
- consultas sobre salsas disponibles;
- recomendaciones sencillas a partir de los datos cargados;
- preguntas frecuentes almacenadas en JSON;
- consulta simulada de pedidos con identificadores `PED-0000`;
- detección básica de solicitudes de información sensible;
- escalamiento verbal cuando la información no está documentada;
- manejo de errores de configuración y de la API;
- pruebas automatizadas sin consumo de créditos de OpenAI.

---

## 3. Menú de demostración de OnigiriDanshi

| Producto | Ingredientes registrados | Precio |
|---|---|---:|
| Spicy Tuna Mayo | Medallón de atún, mayonesa spicy | $80 MXN |
| Salmon Queso Crema | Salmón a la plancha, queso crema, soya | $80 MXN |
| Chicken Teriyaki | Pechuga de pollo en salsa teriyaki | $80 MXN |
| Kinoko Teriyaki | Mezcla de hongos en salsa teriyaki | $80 MXN |
| Crispy Char Siu | Carne molida de cerdo frita en salsa char siu | $80 MXN |

Todos los onigiris registrados tienen un precio de **$80 MXN**.

### Salsas disponibles

- Anguila
- Soya
- Aderezo Chipotle
- Sriracha

La composición interna de estas salsas no está documentada en esta versión del proyecto. Por ello, FoodLabsAI no debe inventar ingredientes o alérgenos de las salsas ni garantizar que un producto sea seguro para una persona con alergias.

---

## 4. Tecnologías utilizadas

- Python 3.10 o posterior
- OpenAI Python SDK
- OpenAI Responses API
- Streamlit
- python-dotenv
- JSON
- Pytest
- Git y GitHub

---

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

### Responsabilidad de los módulos principales

- `app.py`: interfaz Streamlit y manejo del estado de la conversación.
- `src/config.py`: lectura y validación de variables de entorno.
- `src/customer_service.py`: búsqueda local de productos, FAQ, salsas y pedidos simulados.
- `src/openai_service.py`: comunicación con la Responses API y manejo de errores.
- `src/prompts.py`: instrucciones del sistema para FoodLabsAI.
- `data/*.json`: información ficticia utilizada como fuente local de verdad.
- `tests/`: pruebas automatizadas que utilizan mocks y datos locales.

---

## 6. Requisitos previos

Antes de ejecutar el proyecto necesitas:

- Python 3.10 o posterior;
- Git;
- una cuenta de OpenAI Platform;
- una API key válida de OpenAI;
- acceso a un modelo compatible con la Responses API;
- cuota o facturación disponible para realizar llamadas reales a la API.

> La suscripción de ChatGPT y el consumo de la API son servicios separados. La aplicación requiere credenciales y cuota de OpenAI Platform.

---

## 7. Crear y activar el entorno virtual

Ejecuta los comandos desde la carpeta raíz del proyecto.

### Linux / WSL

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Si PowerShell bloquea temporalmente la activación:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Cuando el entorno esté activo, normalmente aparecerá `(.venv)` en la terminal.

---

## 8. Instalar dependencias

Con el entorno virtual activo:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

El archivo `requirements.txt` contiene todas las librerías necesarias para ejecutar la aplicación y sus pruebas.

---

## 9. Configurar variables de entorno

El repositorio incluye `.env.example`, pero **no incluye `.env`**, porque `.env` contiene credenciales privadas y está excluido mediante `.gitignore`.

### Linux / WSL

```bash
cp .env.example .env
```

### Windows PowerShell

```powershell
Copy-Item .env.example .env
```

Edita `.env` y agrega tus valores reales:

```env
OPENAI_API_KEY=tu_api_key_real
OPENAI_MODEL=un_modelo_disponible_en_tu_cuenta
```

Nunca publiques, compartas ni subas `OPENAI_API_KEY` a GitHub.

### Verificación segura de configuración

Puedes comprobar que ambas variables fueron cargadas sin imprimir la API key:

```bash
python -c "from src.config import load_settings; s=load_settings(); print('Modelo:', s.openai_model); print('API key detectada:', bool(s.openai_api_key))"
```

---

## 10. Ejecutar la aplicación

Desde la raíz del proyecto, con `.venv` activo:

```bash
python -m streamlit run app.py
```

Streamlit mostrará una dirección local. Normalmente será:

```text
http://localhost:8501
```

Abre esa dirección en el navegador para interactuar con FoodLabsAI.

Para detener la aplicación desde la terminal utiliza:

```text
Ctrl + C
```

---

## 11. Uso de la interfaz

FoodLabsAI recibe consultas escritas en lenguaje natural. Antes de generar una respuesta, la aplicación busca información relevante en sus archivos JSON y utiliza esos datos como contexto interno para el LLM.

Ejemplos de preguntas:

```text
¿Qué onigiris tienen?
```

```text
¿Cuánto cuesta el Spicy Tuna Mayo?
```

```text
¿Qué ingredientes tiene el Salmon Queso Crema?
```

```text
¿Qué salsas manejan?
```

```text
¿Dónde está mi pedido?
```

```text
¿Cuál es el estado del pedido PED-1001?
```

```text
Quiero hablar con una persona.
```

La interfaz incluye un botón **Limpiar conversación** para reiniciar el historial de la sesión.

---

## 12. Ejemplos de comportamiento esperado

### Producto registrado

Entrada:

```text
¿Cuánto cuesta el Spicy Tuna Mayo?
```

Comportamiento esperado: FoodLabsAI debe indicar que cuesta **$80 MXN**.

### Producto inexistente

Entrada:

```text
¿Tienen onigiri de camarón?
```

Comportamiento esperado: debe indicar que ese producto no está registrado en el menú actual. No debe inventarlo.

### Información no documentada

Entrada:

```text
¿Hacen entregas a Rosarito?
```

Comportamiento esperado: debe reconocer que no cuenta con esa información y ofrecer escalamiento, en lugar de inventar una política de entrega.

### Contexto conversacional

Primero:

```text
¿Qué ingredientes tiene el Spicy Tuna Mayo?
```

Después, dentro de la misma conversación:

```text
¿Cuánto cuesta?
```

FoodLabsAI debe interpretar que la segunda pregunta continúa refiriéndose al Spicy Tuna Mayo.

---

## 13. Consulta simulada de clientes y pedidos

FoodLabsAI **no se conecta a una base de datos real**.

Los clientes y pedidos utilizados para la demostración se encuentran en:

```text
data/customers.json
```

Si el usuario pregunta:

```text
¿Dónde está mi pedido?
```

FoodLabsAI debe solicitar un identificador con formato:

```text
PED-0000
```

Por ejemplo:

```text
PED-1001
```

Cuando se realiza una consulta válida, la terminal debe mostrar:

```text
Consultando base de datos de clientes...
```

Esta salida demuestra la funcionalidad solicitada por la actividad académica.

La aplicación únicamente **consulta datos ficticios**. No cancela, modifica, crea ni reembolsa pedidos reales.

---

## 14. Ejecutar pruebas automatizadas

Las pruebas utilizan datos locales, clientes falsos y mocks. No realizan llamadas reales a OpenAI y, por lo tanto, no consumen créditos de API.

Ejecuta:

```bash
python -m pytest
```

También puedes utilizar:

```bash
pytest
```

Resultado esperado para esta versión:

```text
16 passed
```

Para ver cada prueba individualmente:

```bash
python -m pytest -v
```

### Cobertura funcional actual

Las 16 pruebas verifican, entre otros escenarios:

- carga correcta de configuración;
- detección de variables de entorno faltantes;
- extracción de identificadores `PED-0000`;
- consulta simulada de pedidos;
- pedido inexistente sin invención de datos;
- detección de información sensible;
- búsqueda de productos del menú;
- recuperación de las cuatro salsas registradas;
- solicitud de ID cuando una consulta de pedido está incompleta;
- manejo de preguntas de negocio no documentadas;
- recuperación de los cinco productos del catálogo;
- escalamiento mediante FAQ;
- uso simulado de Responses API;
- respuesta vacía del modelo;
- error de autenticación simulado;
- error de cuota o rate limit simulado.

---

## 15. Validación funcional con el LLM real

Además de las pruebas automatizadas, se realizaron pruebas manuales utilizando Streamlit y una llamada real a la API de OpenAI.

| Escenario | Resultado esperado | Estado |
|---|---|---|
| Consultar el menú | Recupera únicamente los cinco onigiris registrados | Validado |
| Consultar `PED-1001` | Recupera el pedido ficticio y ejecuta la simulación en terminal | Validado |
| Preguntar por onigiri de camarón | Reconoce que no está registrado y no lo inventa | Validado |
| Preguntar por entregas a Rosarito | Reconoce que la política no está documentada y ofrece escalamiento | Validado |

Estas pruebas manuales sí pueden consumir API porque utilizan el modelo configurado en `.env`.

---

## 16. Manejo de errores comunes

### `python: command not found`

Fuera del entorno virtual, algunas distribuciones de Linux/WSL utilizan `python3`:

```bash
python3 --version
```

Para crear el entorno:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Dentro de `.venv`, el comando `python` debe estar disponible.

### `No module named streamlit`, `dotenv`, `openai` o `pytest`

Activa el entorno e instala las dependencias:

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
```

### Faltan `OPENAI_API_KEY` y `OPENAI_MODEL`

Comprueba que `.env` exista en la raíz del proyecto:

```bash
ls -la
```

Si no existe:

```bash
cp .env.example .env
```

Después completa sus valores.

### Error `401`

La API key es inválida, fue revocada o no tiene autorización para el proyecto utilizado.

### Error `429` / `insufficient_quota`

La solicitud llegó a OpenAI, pero el proyecto no tiene cuota suficiente. Revisa la configuración de Usage y Billing en OpenAI Platform.

### Modelo no disponible

Actualiza `OPENAI_MODEL` en `.env` utilizando un modelo disponible para tu proyecto y compatible con la Responses API.

### Streamlit muestra información de una conversación anterior

Utiliza **Limpiar conversación** o reinicia la aplicación:

```text
Ctrl + C
```

```bash
python -m streamlit run app.py
```

---

## 17. Seguridad y privacidad

FoodLabsAI implementa las siguientes medidas básicas:

- la API key se almacena únicamente en `.env`;
- `.env` está excluido de Git mediante `.gitignore`;
- `.env.example` contiene solamente valores de ejemplo;
- las pruebas automatizadas no requieren una API key real;
- los clientes y pedidos son ficticios;
- FoodLabsAI no solicita contraseñas;
- no solicita CVV, NIP ni números completos de tarjetas;
- no solicita información bancaria sensible;
- no inventa productos, precios, pedidos o políticas cuando no están documentados;
- no garantiza seguridad alimentaria cuando no existe información suficiente;
- no garantiza ausencia de contaminación cruzada;
- no ejecuta reembolsos, cancelaciones, cambios ni tickets reales;
- las consultas de pedidos se describen como simulaciones académicas.

---

## 18. Limitaciones conocidas

Esta versión es una demostración académica y presenta limitaciones deliberadas:

- no utiliza una base de datos persistente;
- los clientes, pedidos, productos y FAQ son ficticios;
- el catálogo está limitado a los productos registrados en los archivos JSON;
- no existe inventario en tiempo real;
- no existen pagos reales;
- no existen cancelaciones o modificaciones reales de pedidos;
- no se crean tickets de soporte reales;
- no se conecta automáticamente con un agente humano;
- las políticas no documentadas no pueden ser respondidas como hechos;
- la composición interna de las salsas no está registrada;
- el historial conversacional dura únicamente durante la sesión de Streamlit;
- el funcionamiento del LLM real depende de disponibilidad de API, modelo, conectividad y cuota.

---

## 19. Consideraciones para evaluación

Una persona evaluadora puede reproducir la demostración siguiendo este orden:

1. Crear y activar un entorno virtual.
2. Ejecutar `python -m pip install -r requirements.txt`.
3. Copiar `.env.example` como `.env`.
4. Configurar su propia `OPENAI_API_KEY` y `OPENAI_MODEL`.
5. Ejecutar `python -m pytest` y confirmar `16 passed`.
6. Ejecutar `python -m streamlit run app.py`.
7. Probar una consulta de menú.
8. Probar una consulta de pedido como `PED-1001`.
9. Confirmar en la terminal el mensaje `Consultando base de datos de clientes...`.
10. Probar una consulta no documentada y verificar que FoodLabsAI no invente la respuesta.

---

## 20. Control de versiones

El proyecto utiliza Git y GitHub para control de versiones.

Antes de realizar un commit se recomienda ejecutar:

```bash
python -m pytest
```

Luego:

```bash
git status
git add .
git commit -m "tipo: descripción breve"
git push
```

Ejemplos de mensajes:

```text
feat: add customer support capability
fix: handle missing OpenAI configuration
test: expand FoodLabsAI regression coverage
docs: update FoodLabsAI execution guide
```

Nunca agregues `.env` al repositorio.
