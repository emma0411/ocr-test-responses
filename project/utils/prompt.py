"""Prompt file"""

prompt = """Analiza la imagen adjunta. La imagen contiene un cuestionario con preguntas numeradas en filas.

Cada fila tiene:
- un número de pregunta
- el texto de la pregunta en español
- una escala de respuesta del 1 al 5, donde solo un número está rodeado/circulado

Tu tarea es extraer únicamente la información que esté claramente marcada. Para cada fila, devuelve:

- numero: número de la pregunta
- pregunta: texto exacto de la pregunta
- respuesta: número que está rodeado

Reglas importantes:
- Considera como respuesta solo el número que esté visualmente rodeado o marcado.
- Si una fila no tiene ningún número claramente rodeado, incluye la fila con "respuesta": null.

No infieras ni adivines respuestas. Mantén el texto original en español

Devuelve el resultado exclusivamente en formato JSON, como una lista de objetos, sin texto adicional. Ejemplo de salida esperada:

[
  {
    "numero": 53,
    "pregunta": "Está triste.",
    "respuesta": 1
  }
]
"""