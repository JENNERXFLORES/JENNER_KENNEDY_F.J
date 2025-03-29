import streamlit as st
import random
import json
import os
from collections import Counter

# Archivo para guardar nombres y votos
DATA_FILE = "data.json"

# Función para cargar datos
def cargar_datos():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"estudiantes": [], "votos": {}, "metodo": None}

# Función para guardar datos
def guardar_datos(datos):
    with open(DATA_FILE, "w") as f:
        json.dump(datos, f)

# Cargar datos actuales
datos = cargar_datos()

# ---- INTERFAZ ----
st.title("📢 Elección de Delegado y Subdelegado")

# Sección 1: Registro de estudiantes
st.subheader("1️⃣ Registro de Estudiantes")
nombre_estudiante = st.text_input("✍️ Ingresa tu nombre para registrarte:")

if st.button("Registrar"):
    if nombre_estudiante and nombre_estudiante not in datos["estudiantes"]:
        datos["estudiantes"].append(nombre_estudiante)
        guardar_datos(datos)
        st.success(f"✅ {nombre_estudiante} ha sido registrado.")
    elif nombre_estudiante in datos["estudiantes"]:
        st.warning("⚠️ Este nombre ya está registrado.")
    else:
        st.warning("⚠️ Ingresa un nombre válido.")

st.write("📜 **Lista de estudiantes registrados:**")
st.write(datos["estudiantes"])

# Sección 2: Elección del método (solo administrador)
st.subheader("2️⃣ Selección del Método (Solo Administrador)")
admin = st.text_input("🔑 Clave de Administrador:", type="password")

if admin == "1234":
    metodo = st.radio("🛠 Método de elección:", ("Aleatorio", "Votación"))

    if st.button("Guardar Método"):
        datos["metodo"] = metodo
        datos["votos"] = {}  # Reiniciar votos si cambia el método
        guardar_datos(datos)
        st.success(f"✅ Método '{metodo}' seleccionado.")

# Sección 3: Votación (si el método es votación)
if datos["metodo"] == "Votación":
    st.subheader("🗳 Votación de Delegado")
    votante = st.text_input("✍️ Ingresa tu nombre para votar:")
    
    if votante in datos["estudiantes"]:
        candidato = st.selectbox("📌 Elige a quién votar:", [e for e in datos["estudiantes"] if e != votante])
        
        if st.button("Votar"):
            datos["votos"][votante] = candidato
            guardar_datos(datos)
            st.success("✅ Tu voto ha sido registrado.")
    else:
        st.warning("⚠️ Solo los estudiantes registrados pueden votar.")

    # Mostrar resultados parciales
    st.subheader("📊 Resultados Parciales")
    conteo_votos = Counter(datos["votos"].values())
    for nombre, num_votos in conteo_votos.most_common():
        st.write(f"🎖 {nombre}: {num_votos} votos")

# Sección 4: Elección final (solo el administrador puede ver)
if admin == "1234" and datos["metodo"]:
    st.subheader("🎯 Elección Final")

    if datos["metodo"] == "Aleatorio":
        if len(datos["estudiantes"]) >= 2:
            delegado, subdelegado = random.sample(datos["estudiantes"], 2)
            st.success(f"🎖 Delegado: {delegado}")
            st.info(f"🥈 Subdelegado: {subdelegado}")
        else:
            st.warning("⚠️ Debe haber al menos 2 estudiantes.")
    
    elif datos["metodo"] == "Votación":
        if datos["votos"]:
            mas_votados = Counter(datos["votos"].values()).most_common(2)
            if len(mas_votados) >= 2:
                st.success(f"🎖 Delegado: {mas_votados[0][0]} con {mas_votados[0][1]} votos")
                st.info(f"🥈 Subdelegado: {mas_votados[1][0]} con {mas_votados[1][1]} votos")
            else:
                st.warning("⚠️ No hay suficientes votos.")
        else:
            st.warning("⚠️ Aún no hay votos registrados.")
