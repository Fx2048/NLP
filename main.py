import os
import streamlit as st
import openai
import pandas as pd  # Para manejar los archivos CSV
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Cargar archivos CSV
carta = pd.read_csv('/mnt/data/lista_carta.csv')  # Cargar carta del restaurante
distritos = pd.read_csv('/mnt/data/distritos_reparto.csv')  # Cargar distritos de reparto
historial = pd.read_csv('/mnt/data/historial_pedido.csv')  # Historial de pedidos

# Función para mostrar la carta
def mostrar_carta():
    return carta.to_string(index=False)

# Verificar si el distrito está disponible para reparto
def verificar_distrito(distrito):
    return distrito in distritos['Distrito'].values

# Guardar el pedido en el historial
def guardar_pedido(pedido):
    nuevo_pedido = pd.DataFrame([pedido])
    nuevo_pedido.to_csv('/mnt/data/historial_pedido.csv', mode='a', header=False, index=False)

# Generar respuesta del chatbot
def generar_respuesta(mensaje):
    messages = [
        {"role": "system", "content": "Eres un asistente que toma pedidos para un restaurante."},
        {"role": "user", "content": mensaje}
    ]
    
    try:
        response = openai.ChatCompletion.create(  
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
accion = st.selectbox("Selecciona una acción", ["Ver Carta", "Tomar Pedido", "Salir"])

if accion == "Ver Carta":
    st.write("Carta del restaurante:")
    st.write(mostrar_carta())

elif accion == "Tomar Pedido":
    nombre = st.text_input("Ingresa tu nombre:")
    pedido = st.text_input("Escribe tu pedido:")
    distrito = st.text_input("Ingresa tu distrito:")
    
    if st.button("Confirmar Pedido"):
        if verificar_distrito(distrito):
            guardar_pedido({"Nombre": nombre, "Pedido": pedido, "Distrito": distrito})
            st.write("¡Pedido confirmado!")
        else:
            st.write("Lo siento, no realizamos entregas en tu distrito.")

elif accion == "Salir":
    st.write("Gracias por usar nuestro servicio. ¡Vuelve pronto!")

