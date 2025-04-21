import streamlit as st
import openai
import re
import time
from datetime import datetime, timedelta

st.title("HydroBot")
st.write("Tu asistente personal para recordarte tomar agua a lo largo del día.")

user_input = st.text_input("¿Cuándo querés que te recuerde tomar agua?", placeholder="Ej: Recordame tomar agua a las 16:30")

prompt_base = (
    "Actuá como un asistente de salud que ayuda a las personas a mantenerse hidratadas. "
    "Cuando el usuario diga algo como 'Recordame tomar agua a las 16:30', "
    "extraé la hora y confirmá el recordatorio de forma amigable."
)

# Función para extraer hora
def extraer_hora(texto):
    coincidencia = re.search(r"(\d{1,2})[:h](\d{2})?", texto)
    if coincidencia:
        hora = int(coincidencia.group(1))
        minutos = int(coincidencia.group(2)) if coincidencia.group(2) else 0
        return hora, minutos
    return None, None

# Lógica principal
if user_input:
    with st.spinner("Procesando tu recordatorio..."):
        try:
            full_prompt = prompt_base + "\n\nUsuario: " + user_input

            # Llamada a la API de OpenAI
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # o "gpt-4" si tenés acceso
                messages=[
                    {"role": "system", "content": prompt_base},
                    {"role": "user", "content": user_input}
                ]
            )
            mensaje = response.choices[0].message["content"]
            st.success(mensaje)

            # Configurar recordatorio
            hora, minutos = extraer_hora(user_input)
            if hora is not None:
                ahora = datetime.now()
                recordatorio_datetime = ahora.replace(hour=hora, minute=minutos, second=0, microsecond=0)
                if recordatorio_datetime < ahora:
                    recordatorio_datetime += timedelta(days=1)

                segundos_espera = (recordatorio_datetime - ahora).total_seconds()
                st.info(f"Te recordaremos tomar agua en {int(segundos_espera // 60)} minutos.")
                with st.spinner("Esperando..."):
                    time.sleep(segundos_espera)
                    st.success(f"¡Es hora de hidratarse!  {user_input}")

        except Exception as e:
            st.error(f"Error: {e}")
