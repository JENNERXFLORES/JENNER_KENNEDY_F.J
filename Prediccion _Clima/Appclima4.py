import streamlit as st
import numpy as np
from hmmlearn import hmm
from sklearn.ensemble import RandomForestClassifier

# Configuración de la aplicación
st.set_page_config(page_title="Explicación HMM + Random Forest", layout="wide")
st.title("📊 Explicación Interactiva del Modelo HMM con Aprendizaje Automático")

# Introducción Detallada
st.write("""
## 📝 Introducción
Este código combina un **Modelo Oculto de Markov (HMM)** con **aprendizaje automático (Random Forest)** para mejorar la predicción del clima.

### 🔍 ¿Qué diferencia este modelo de los anteriores?
- **Usa un HMM** para modelar la transición entre estados climáticos.
- **Agrega un Random Forest** para predecir el clima basándose en características como temperatura, humedad y presión.
- **Permite mejorar la predicción combinando modelos estadísticos y aprendizaje automático.**

### 📌 ¿Cómo funciona?
1. Se define la matriz de transición y el modelo HMM.
2. Se entrena el modelo con datos de observaciones del clima.
3. Se usa el **algoritmo de Viterbi** para predecir la secuencia de estados ocultos.
4. Se entrena un **Random Forest** con características meteorológicas.
5. Se hace una predicción combinada para determinar el estado climático.
""")

states = ["Soleado", "Nublado", "Lluvioso"]

if st.button("📌 Paso 1: Importar Librerías"):
    st.code("""
import numpy as np
from hmmlearn import hmm
from sklearn.ensemble import RandomForestClassifier
    """, language="python")
    st.write("Este código usa librerías para modelos probabilísticos y aprendizaje automático:")
    st.write("- **`hmmlearn`**: Para el modelo de Markov.")
    st.write("- **`sklearn.ensemble.RandomForestClassifier`**: Para mejorar la predicción con aprendizaje automático.")

if st.button("📊 Paso 2: Definir los Estados y la Matriz de Transición"):
    st.code("""
states = ["Soleado", "Nublado", "Lluvioso"]
n_states = len(states)

transition_matrix = np.array([
    [0.6, 0.3, 0.1],
    [0.3, 0.4, 0.3],
    [0.2, 0.3, 0.5]
])
    """, language="python")
    st.write("Definimos los estados del clima y la matriz de transición que modela los cambios entre ellos.")

if st.button("🤖 Paso 3: Crear y Entrenar el Modelo HMM"):
    st.code("""
model = hmm.MultinomialHMM(n_components=3)
model.startprob_ = np.array([0.6, 0.3, 0.1])
model.transmat_ = transition_matrix

observations = np.array([[0, 1, 2, 0, 0, 1, 2, 2]]).T
model.fit(observations)
    """, language="python")
    st.write("Se crea un **Modelo HMM** y se entrena con datos de observación del clima.")

if st.button("🔍 Paso 4: Predecir la Secuencia de Estados Ocultos"):
    st.code("""
logprob, hidden_states_sequence = model.decode(observations, algorithm="viterbi")
    """, language="python")
    st.write("Se usa el **algoritmo de Viterbi** para encontrar la secuencia más probable de estados ocultos.")

if st.button("📡 Paso 5: Entrenar el Random Forest con Datos Meteorológicos"):
    st.code("""
features = np.array([
    [25, 70, 1013],  # Soleado
    [18, 80, 1005],  # Nublado
    [15, 90, 1000],  # Lluvioso
    [30, 65, 1018],  # Soleado
    [20, 75, 1010],  # Nublado
    [17, 85, 1002]   # Lluvioso
])
labels = np.array([0, 1, 2, 0, 1, 2])

clf = RandomForestClassifier()
clf.fit(features, labels)
    """, language="python")
    st.write("Se entrena un modelo de **Random Forest** con datos meteorológicos.")

if st.button("🚀 Paso 6: Ejecutar Predicción en Vivo"):
    features = np.array([
        [25, 70, 1013],
        [18, 80, 1005],
        [15, 90, 1000],
        [30, 65, 1018],
        [20, 75, 1010],
        [17, 85, 1002]
    ])
    labels = np.array([0, 1, 2, 0, 1, 2])
    
    clf = RandomForestClassifier()
    clf.fit(features, labels)
    
    new_data = np.array([[22, 75, 1010]])
    predicted_label = clf.predict(new_data)
    predicted_label = int(predicted_label[0])  # Convertimos a entero estándar
    
    st.write("### 🔥 Resultado de la Predicción:")
    st.write(f"**Condición climática predicha:** {states[predicted_label]}")