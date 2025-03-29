import numpy as np
from hmmlearn import hmm
from sklearn.ensemble import RandomForestClassifier

# 1. Definición de los estados y la matriz de transición para una cadena de Markov
states = ["Soleado", "Nublado", "Lluvioso"]
n_states = len(states)

# Matriz de transición de ejemplo para la cadena de Markov
transition_matrix = np.array([
    [0.6, 0.3, 0.1],  # Soleado
    [0.3, 0.4, 0.3],  # Nublado
    [0.2, 0.3, 0.5]   # Lluvioso
])

print("Matriz de transición:")
print(transition_matrix)

# 2. Definición del modelo oculto de Markov (HMM)
hidden_states = ["Patrón A", "Patrón B", "Patrón C"]
n_hidden_states = len(hidden_states)

# Probabilidades de inicio para los estados ocultos
start_prob = np.array([0.6, 0.3, 0.1])
# Matriz de transición entre estados ocultos
trans_matrix = np.array([
    [0.7, 0.2, 0.1],
    [0.3, 0.5, 0.2],
    [0.2, 0.3, 0.5]
])

# Matriz de emisión (probabilidad de observaciones dadas los estados ocultos)
emission_matrix = np.array([
    [0.8, 0.1, 0.1],  # Patrón A emite Soleado, Nublado, Lluvioso
    [0.2, 0.6, 0.2],  # Patrón B emite Soleado, Nublado, Lluvioso
    [0.1, 0.1, 0.8]   # Patrón C emite Soleado, Nublado, Lluvioso
])

# Creación del modelo HMM
model = hmm.MultinomialHMM(n_components=n_hidden_states)
model.startprob_ = start_prob
model.transmat_ = trans_matrix
model.emissionprob_ = emission_matrix

print("Modelo HMM creado.")

# 3. Entrenamiento del modelo HMM con datos de observación (históricos)
# Observaciones: Soleado (0), Nublado (1), Lluvioso (2)
observations = np.array([[0, 1, 2, 0, 0, 1, 2, 2]]).T

# Entrenamiento del modelo HMM
model.fit(observations)
print("Modelo HMM entrenado.")

# 4. Predicción de la secuencia de estados ocultos
logprob, hidden_states_sequence = model.decode(observations, algorithm="viterbi")
print("Secuencia de estados ocultos predicha:")
print(hidden_states_sequence)

# 5. Mejora del modelo con aprendizaje automático
# Ejemplo de características (Temp, Humedad, Presión) y etiquetas (Soleado, Nublado, Lluvioso)
features = np.array([
    [25, 70, 1013],  # Soleado
    [18, 80, 1005],  # Nublado
    [15, 90, 1000],  # Lluvioso
    [30, 65, 1018],  # Soleado
    [20, 75, 1010],  # Nublado
    [17, 85, 1002]   # Lluvioso
])
labels = np.array([0, 1, 2, 0, 1, 2])  # Soleado, Nublado, Lluvioso

# Entrenamiento de un modelo de clasificación (Random Forest)
clf = RandomForestClassifier()
clf.fit(features, labels)

# Predicción con el modelo de clasificación
new_data = np.array([[22, 75, 1010]])  # Nuevos datos de observación
predicted_label = clf.predict(new_data)
print("Condición climática predicha:", states[predicted_label[0]])
