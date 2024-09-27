import os
import streamlit as st
import openai
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Moderación de OpenAI
def moderar_contenido(input_text):
    response = openai.Moderation.create(input=input_text)
    results = response['results'][0]
    
    if results['flagged']:
        return f"Mensaje moderado: {', '.join([k for k, v in results['categories'].items() if v])}"
    return None

# Generar respuesta del chatbot
def generar_respuesta(mensaje):
    moderacion = moderar_contenido(mensaje)
    if moderacion:
        return moderacion
    
    messages = [
        {"role": "system", "content": "Eres un asistente que toma pedidos para un restaurante."},
        {"role": "user", "content": mensaje}
    ]
    
    try:
        response = openai.ChatCompletion.create(  # Este es el método correcto
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=150
        )
        return response.choices[0].message["content"]
    
    except openai.error.OpenAIError as e:
        return f"Error en la API: {str(e)}"

# Interfaz en Streamlit
st.title("Chatbot para tomar pedidos en un restaurante")
st.write("Escribe tu pedido a continuación:")

# Entrada de texto del usuario
mensaje_usuario = st.text_input("Mensaje:")

# Botón para enviar el mensaje
if st.button("Enviar"):
    respuesta = generar_respuesta(mensaje_usuario)
    st.write(f"Respuesta: {respuesta}")



