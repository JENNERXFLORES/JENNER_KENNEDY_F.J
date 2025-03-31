import streamlit as st
import random
import json
import os
from collections import Counter

# Archivo para guardar nombres y votos
DATA_FILE = "data.json"

# Función para cargar datos (conversión de votantes de lista a set)
def cargar_datos():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            datos = json.load(f)
            # Convertir de lista a set si existe la clave "votantes"
            datos["votantes"] = set(datos.get("votantes", []))
            return datos
    return {"estudiantes": [], "votos": {}, "metodo": None, "votacion_activa": False, 
            "mostrar_resultados": False, "delegado": None, "subdelegado": None, "votantes": set()}

# Función para guardar datos (conversión de votantes de set a lista)
def guardar_datos(datos):
    datos_a_guardar = datos.copy()
    datos_a_guardar["votantes"] = list(datos["votantes"])
    with open(DATA_FILE, "w") as f:
        json.dump(datos_a_guardar, f)

# Cargar datos actuales
datos = cargar_datos()

# Inicialización de variables en session_state
if "rol" not in st.session_state:
    st.session_state["rol"] = None
if "mostrar_metodo" not in st.session_state:
    st.session_state["mostrar_metodo"] = False

# ---- INTERFAZ ----
st.title("📢 Elección de Delegado y Subdelegado")

# Selección de tipo de usuario
st.subheader("Selecciona tu rol:")
col1, col2 = st.columns(2)

with col1:
    if st.button("👨‍🎓 Alumno"):
        st.session_state["rol"] = "Alumno"

with col2:
    if st.button("🔧 Administrador"):
        st.session_state["rol"] = "Administrador"

if st.session_state["rol"]:
    if st.session_state["rol"] == "Alumno":
        st.subheader("Registro / Votación de Estudiantes")
        # Si aún no se ha configurado el método (ni votación activa ni resultados), se muestra el formulario de registro
        if not datos["votacion_activa"] and not datos["mostrar_resultados"]:
            st.info("Regístrate para participar en la elección.")
            nombre_estudiante = st.text_input("✍️ Ingresa tu nombre para registrarte:")
            if st.button("Registrar"):
                if nombre_estudiante:
                    if nombre_estudiante not in datos["estudiantes"]:
                        datos["estudiantes"].append(nombre_estudiante)
                        guardar_datos(datos)
                        st.success(f"✅ {nombre_estudiante} ha sido registrado.")
                    else:
                        st.warning("⚠️ Este nombre ya está registrado.")
                else:
                    st.warning("⚠️ Ingresa un nombre válido.")
            st.write("📜 **Lista de estudiantes registrados:**")
            st.write(datos["estudiantes"])
        else:
            # Una vez configurado el método, el alumno ingresa su nombre para votar o ver resultados
            nombre_estudiante = st.text_input("✍️ Ingresa tu nombre para votar o ver resultados:")
            if not nombre_estudiante:
                st.warning("⚠️ Ingresa tu nombre para continuar.")
            elif nombre_estudiante not in datos["estudiantes"]:
                st.warning("⚠️ No estás registrado. Contacta al administrador para registrarte.")
            else:
                if datos["votacion_activa"]:
                    st.subheader("🗳 Votación en Proceso")
                    if nombre_estudiante not in datos["votantes"]:
                        voto = st.selectbox("Elige un delegado:", datos["estudiantes"])
                        if st.button("Votar"):
                            datos["votos"][nombre_estudiante] = voto
                            datos["votantes"].add(nombre_estudiante)
                            guardar_datos(datos)
                            st.success("✅ Voto registrado correctamente.")
                    else:
                        st.info("Ya has votado.")
                elif datos["mostrar_resultados"]:
                    st.info("La elección ya ha finalizado. Consulta los resultados a continuación.")
                    st.subheader("🏆 Resultados de la Elección")
                    st.success(f"🎖 Delegado: {datos['delegado']}")
                    st.info(f"🥈 Subdelegado: {datos['subdelegado']}")
                    # Mostrar el recuento final de votos
                    if datos["votos"]:
                        conteo_votos = Counter(datos["votos"].values())
                        st.write("**Resultados de votos:**")
                        for candidato, cant in conteo_votos.most_common():
                            st.write(f"{candidato}: {cant} voto(s)")
        # Botón para recargar la página y ver cambios en tiempo real
        if st.button("🔄 Recargar Página"):
            datos = cargar_datos()
            st.rerun()
            
    elif st.session_state["rol"] == "Administrador":
        admin = st.text_input("🔑 Clave de Administrador:", type="password")
        if admin == "1234":
            st.subheader("2️⃣ Verificación de Registro")
            if st.button("🔄 Actualizar Lista"):
                datos = cargar_datos()
                st.rerun()
            st.write("📜 **Lista de estudiantes registrados:**")
            st.write(datos["estudiantes"])
            if len(datos["estudiantes"]) >= 2:
                if st.button("✅ Continuar"):
                    st.session_state["mostrar_metodo"] = True
            else:
                st.warning("⚠️ Debe haber al menos 2 estudiantes registrados para continuar.")
            if st.session_state["mostrar_metodo"]:
                st.subheader("3️⃣ Selección del Método")
                # Usamos key para mantener el valor seleccionado entre reruns
                metodo = st.radio("🛠 Método de elección:", ("Aleatorio", "Votación"), key="metodo_radio")
                if st.button("Guardar Método"):
                    datos["metodo"] = metodo
                    datos["votos"] = {}
                    datos["votacion_activa"] = (metodo == "Votación")
                    datos["votantes"] = set()  # Reiniciar votantes al cambiar el método
                    if metodo == "Aleatorio" and len(datos["estudiantes"]) >= 2:
                        datos["delegado"], datos["subdelegado"] = random.sample(datos["estudiantes"], 2)
                        datos["mostrar_resultados"] = True
                    guardar_datos(datos)
                    st.success(f"✅ Método '{metodo}' seleccionado.")
                    st.rerun()
                if metodo == "Votación":
                    st.info("🗳 La votación ha sido activada. Los alumnos pueden votar ahora.")
                    st.write(f"Votantes registrados: {len(datos['votantes'])} / {len(datos['estudiantes'])}")
                    if st.button("Finalizar Votación y Mostrar Resultados", disabled=(len(datos['votantes']) < len(datos['estudiantes']))):
                        if datos["votos"]:
                            conteo_votos = Counter(datos["votos"].values())
                            # Delegado es el candidato con más votos
                            delegado, _ = conteo_votos.most_common(1)[0]
                            # Buscar candidatos para subdelegado (excluyendo al delegado)
                            subdelegados_posibles = [c for c, v in conteo_votos.items() if c != delegado]
                            subdelegado = None
                            if subdelegados_posibles:
                                max_votos = max(conteo_votos[c] for c in subdelegados_posibles)
                                candidatos_sub = [c for c in subdelegados_posibles if conteo_votos[c] == max_votos]
                                subdelegado = random.choice(candidatos_sub)
                            datos["delegado"] = delegado
                            datos["subdelegado"] = subdelegado
                            datos["mostrar_resultados"] = True
                            # Se desactiva la votación para que los alumnos vean los resultados
                            datos["votacion_activa"] = False
                            guardar_datos(datos)
                            st.success("✅ Votación finalizada y resultados calculados.")
                            # Mostrar el recuento final de votos en la vista de administrador
                            st.write("**Resultados de votos:**")
                            for candidato, cant in conteo_votos.most_common():
                                st.write(f"{candidato}: {cant} voto(s)")
                            st.rerun()
                        else:
                            st.warning("⚠️ No se registraron votos.")
                    elif len(datos['votantes']) < len(datos['estudiantes']):
                        st.warning("⚠️ Aún no todos los alumnos han votado.")
            if datos["mostrar_resultados"]:
                st.subheader("🏆 Resultados de la Elección")
                st.success(f"🎖 Delegado: {datos['delegado']}")
                st.info(f"🥈 Subdelegado: {datos['subdelegado']}")
                # Mostrar el recuento final de votos
                if datos["votos"]:
                    conteo_votos = Counter(datos["votos"].values())
                    st.write("**Resultados de votos:**")
                    for candidato, cant in conteo_votos.most_common():
                        st.write(f"{candidato}: {cant} voto(s)")
            if st.button("🧹 Limpiar Lista de Estudiantes"):
                datos = {"estudiantes": [], "votos": {}, "metodo": None, "votacion_activa": False, 
                         "mostrar_resultados": False, "delegado": None, "subdelegado": None, "votantes": set()}
                guardar_datos(datos)
                st.success("✅ Lista de estudiantes eliminada.")
                st.rerun()
            if st.button("🔄 Reiniciar Todo"):
                datos = {"estudiantes": [], "votos": {}, "metodo": None, "votacion_activa": False, 
                         "mostrar_resultados": False, "delegado": None, "subdelegado": None, "votantes": set()}
                guardar_datos(datos)
                st.success("✅ Se ha reiniciado la elección.")
                st.rerun()
            # Botón para recargar la página y ver cambios en tiempo real
            if st.button("🔄 Recargar Página"):
                datos = cargar_datos()
                st.rerun()
        else:
            st.warning("🔒 Clave de administrador incorrecta.")
