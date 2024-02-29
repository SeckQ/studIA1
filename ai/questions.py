import os
from flask import Blueprint, request, jsonify
import openai
from dotenv import load_dotenv


load_dotenv('./secrets/.env')
ai_bp = Blueprint('openai', __name__)

openai.api_key = os.getenv('OPENAI_API_KEY')



def generar_preguntas_y_respuestas_ia(text, quantity=3, temperature=0.8):
    prompt = f"Genera {quantity} preguntas de opción múltiple y sus respuestas para el siguiente texto:\n\n{text}\nDame la respuesta con las siguientes etiquetas: Pregunta:, Opciones: y dentro de esto cada opcion con Opcion N#:, Respuesta correcta:\n\nPreguntas y respuestas:"

    response = openai.ChatCompletion.create(
        model=os.getenv('OPENAI_MODEL'),
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens = int(os.getenv('OPENAI_MAX_TOKENS')),
        temperature=float(os.getenv('OPENAI_TEMPERATURE')),
        n=1,
    )

    preguntas_y_respuestas_generadas = [choice['message']['content'].strip() for choice in response.choices]

    #print("Respuesta de OpenAI:", preguntas_y_respuestas_generadas)

    return preguntas_y_respuestas_generadas


@ai_bp.route('/generate-questions', methods=['POST'])
def generar_preguntas_respuestas():
    data = request.json
    text = data['text']
    quantity = data.get('quantity', 2)
    temperature = data.get('temperature', 0.8)

    preguntas_y_respuestas_generadas = generar_preguntas_y_respuestas_ia(text, quantity, temperature)

    array_respuestas = procesar_respuestas(preguntas_y_respuestas_generadas)
    print(preguntas_y_respuestas_generadas)

    return jsonify({'preguntas_y_respuestas': array_respuestas})


def procesar_respuestas(respuestas):
    array_respuestas = []
    for i, respuesta in enumerate(respuestas, 1):
        preguntas_respuestas = parsear_respuesta(respuesta)
        array_respuestas.extend(preguntas_respuestas)
    return array_respuestas


def parsear_respuesta(respuesta):
    lines = respuesta.split("\n")
    preguntas_respuestas = []
    pregunta = None
    opciones = []
    respuesta_correcta_id = None

    for line in lines:
        if line.startswith("Pregunta:"):
            if pregunta:
                preguntas_respuestas.append({
                    "Pregunta": pregunta,
                    "Opciones": opciones,
                    "Respuesta correcta": respuesta_correcta_id
                })
            pregunta = line.split(": ")[1].strip()
            opciones = []
            respuesta_correcta_id = None
        elif line.startswith("Opción "):
            opcion_id = int(line.split(": ")[0].split(" ")[1])
            opcion_texto = line.split(": ")[1].strip()
            opciones.append({"id": opcion_id, "texto": opcion_texto})
        elif line.startswith("Respuesta correcta:"):
            respuesta_correcta_id = int(line.split(": ")[1].split(":")[0].split(" ")[1])

    if pregunta:
        preguntas_respuestas.append({
            "Pregunta": pregunta,
            "Opciones": opciones,
            "Respuesta correcta": respuesta_correcta_id
        })
    print(preguntas_respuestas)
    return preguntas_respuestas

