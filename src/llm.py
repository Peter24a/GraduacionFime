import requests

OLLAMA_URL = "http://host.docker.internal:11434/api/chat"
MODEL = "lfm2:latest"


def generar_resumen_graduacion(datos: dict) -> str:
    prompt = f"""Eres el asistente de la fiesta de graduación de FIME (UANL).
Un egresado acaba de registrarse. Con base en sus datos, genera un resumen breve (máximo 150 palabras) en español, tono entusiasta, de cómo podría verse su graduación e incluye una estimación de costo total. Sin viñetas ni encabezados, solo texto corrido.

Datos: {datos}"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={"model": MODEL, "messages": [{"role": "user", "content": prompt}], "stream": False},
            timeout=60,
        )
        response.raise_for_status()
        return response.json()["message"]["content"]
    except Exception as e:
        return f"(No se pudo generar el resumen: {e})"
