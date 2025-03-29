import streamlit as st
import subprocess

def ejecutar_turtle():
    # Ejecuta el código de Turtle en un proceso separado
    subprocess.run(["python", "girasol.py"])  

st.title("Girasol con Turtle en Vivo 🌻")

st.write("Haz clic en el botón para ejecutar el código en una ventana separada.")

if st.button("Ejecutar Girasol"):
    ejecutar_turtle()

