import numpy as np
import pandas as pd
from hmmlearn import hmm
from sklearn.preprocessing import LabelEncoder

# Simulando datos históricos de clima
data = {
    'Estado': ['Soleado', 'Nublado', 'Lluvioso', 'Soleado', 'Nublado', 'Lluvioso', 'Lluvioso', 'Soleado', 'Soleado']
}
df = pd.DataFrame(data)

# Codificación de los estados del clima
le = LabelEncoder()
df['Estado_encoded'] = le.fit_transform(df['Estado'])
X = df['Estado_encoded'].values.reshape(-1, 1)

# Configuración del modelo oculto de Markov
model = hmm.MultinomialHMM(n_components=3, n_iter=100)
model.fit(X)

# Predicción del próximo estado del clima
logprob, next_state = model.decode(X, algorithm="viterbi")
predicted_state = model.predict([[next_state[-1]]])
predicted_climate = le.inverse_transform(predicted_state)

print("El próximo estado del clima predicho es:", predicted_climate[0])
