import streamlit as st
import numpy as np
import pandas as pd
from hmmlearn import hmm
from sklearn.preprocessing import LabelEncoder

# Título de la presentación
st.title("🌦️ Predicción del Clima con Modelos Ocultos de Markov")

st.write("""
Este programa usa un **Modelo Oculto de Markov (HMM)** para predecir el clima del próximo día  
basándose en datos históricos. Analiza patrones en los estados del clima **(Soleado, Nublado, Lluvioso)**  
y genera una predicción.  
         
🔹 Diferencias clave con los otros códigos:
         
✅ Solo trabaja con los estados del clima (Soleado, Nublado, Lluvioso), no usa temperatura ni humedad.   
✅ No tiene una matriz de emisión como en el Código 1 o 4.         
✅ Usa LabelEncoder para convertir nombres de estados a números.               
✅ Predice un solo estado futuro, no una secuencia completa.
""")

# Paso 1: Importar librerías
if st.button("📌 Paso 1: Importar librerías"):
    st.code("""
import numpy as np
import pandas as pd
from hmmlearn import hmm
from sklearn.preprocessing import LabelEncoder
""", language="python")
    st.write("""
- **`numpy`**: Maneja cálculos numéricos.  
- **`pandas`**: Permite trabajar con datos tabulares.  
- **`hmmlearn`**: Se usa para construir y entrenar el Modelo Oculto de Markov (HMM).  
- **`LabelEncoder`**: Convierte los nombres de los estados del clima a valores numéricos.  
""")

# Paso 2: Crear datos históricos del clima
if st.button("🌦️ Paso 2: Crear datos históricos del clima"):
    st.code("""
data = {
    'Estado': ['Soleado', 'Nublado', 'Lluvioso', 'Soleado', 'Nublado', 
               'Lluvioso', 'Lluvioso', 'Soleado', 'Soleado']
}
df = pd.DataFrame(data)
""", language="python")
    st.write("""
Se crea un conjunto de datos simulando 9 días de clima pasado.  

📌 **Ejemplo de la tabla de datos históricos:**  
| Día  | Estado  |  
|------|---------|  
| 1    | Soleado |  
| 2    | Nublado |  
| 3    | Lluvioso |  
| ...  | ...     |  
""")

# Paso 3: Convertir los estados del clima a números
if st.button("🔢 Paso 3: Convertir estados del clima a números"):
    st.code("""
le = LabelEncoder()
df['Estado_encoded'] = le.fit_transform(df['Estado'])
X = df['Estado_encoded'].values.reshape(-1, 1)
""", language="python")
    st.write("""
El **LabelEncoder** convierte cada estado del clima en un número:  
- **Soleado** → 2  
- **Nublado** → 1  
- **Lluvioso** → 0  
Esto permite que el modelo trabaje con los datos numéricos.  

📌 **Ejemplo de conversión:**  
| Estado  | Estado_encoded |  
|---------|---------------|  
| Soleado | 2             |  
| Nublado | 1             |  
| Lluvioso | 0             |  
""")

# Paso 4: Crear el Modelo Oculto de Markov (HMM)
if st.button("🧠 Paso 4: Configurar el Modelo HMM"):
    st.code("""
model = hmm.MultinomialHMM(n_components=3, n_iter=100)
model.fit(X)
""", language="python")
    st.write("""
- Se configura un **Modelo Oculto de Markov (HMM)** con **3 estados** (Soleado, Nublado, Lluvioso).  
- **Entrenamiento**: El modelo analiza la secuencia de datos históricos para aprender los patrones de transición.  
""")

# Paso 5: Predicción del próximo estado del clima
if st.button("🔮 Paso 5: Predecir el próximo estado del clima"):
    st.code("""
logprob, next_state = model.decode(X, algorithm="viterbi")
predicted_state = model.predict([[next_state[-1]]])
predicted_climate = le.inverse_transform(predicted_state)
""", language="python")
    st.write("""
- **`model.decode(X, algorithm="viterbi")`** encuentra la secuencia de estados más probable.  
- **`model.predict()`** predice el próximo estado basado en los datos aprendidos.  
- **`le.inverse_transform()`** convierte el número predicho de vuelta a su nombre original (Soleado, Nublado o Lluvioso).  
""")

# Paso 6: Ejecutar todo el código y mostrar el resultado
if st.button("🚀 Paso 6: Ejecutar Código Completo"):
    # Creación de datos
    data = {
        'Estado': ['Soleado', 'Nublado', 'Lluvioso', 'Soleado', 'Nublado', 
                   'Lluvioso', 'Lluvioso', 'Soleado', 'Soleado']
    }
    df = pd.DataFrame(data)

    # Codificación de los estados
    le = LabelEncoder()
    df['Estado_encoded'] = le.fit_transform(df['Estado'])
    X = df['Estado_encoded'].values.reshape(-1, 1)

    # Configuración del HMM
    model = hmm.MultinomialHMM(n_components=3, n_iter=100)
    model.fit(X)

    # Predicción del próximo estado
    logprob, next_state = model.decode(X, algorithm="viterbi")
    predicted_state = model.predict([[next_state[-1]]])
    predicted_climate = le.inverse_transform(predicted_state)

    # Mostrar resultado en Streamlit
    st.success(f"🌤️ El próximo estado del clima predicho es: **{predicted_climate[0]}**")

    st.write("""
### 📊 **Explicación del resultado**
- El modelo ha aprendido de los datos históricos y ha predicho el clima para el siguiente día.
- La predicción se basa en la **secuencia de cambios climáticos** observada en los días anteriores.
- Si ejecutas el código varias veces con diferentes datos, podrías obtener distintos resultados.
""")

