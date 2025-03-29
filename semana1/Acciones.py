#Este programa simula el valor del dólar en soles peruanos 
# para los próximos 15 días, basándose en datos históricos de 
# variaciones diarias.

import random

# Datos históricos del valor del dólar en soles peruanos (Fecha, Día, Precio cierre, Variación %, Precio mínimo, Precio máximo)
datos_dolar = [
    ("2024-08-30", "Viernes", 3.748, 0.00, 3.747, 3.750),
    ("2024-08-29", "Jueves", 3.748, 0.15, 3.738, 3.748),
    ("2024-08-28", "Miércoles", 3.743, 0.00, 3.739, 3.746),
    ("2024-08-27", "Martes", 3.743, -0.41, 3.743, 3.758),
    ("2024-08-26", "Lunes", 3.758, 0.25, 3.716, 3.758),
    ("2024-08-23",  "Viernes",  3.749,0.15, 3.743,  3.759),
    ("2024-08-22",  "Jueves",   3.743,  -0.20,  3.743,  3.758),
("2024-08-21",  "Miércoles",    3.751   ,0.11   ,3.727, 3.753),
("2024-08-20"   ,"Martes"   ,3.746  ,0.37   ,3.720  ,3.746),
("2024-08-19",  "Lunes",    3.733,  -0.13   ,3.730, 3.747),
("2024-08-16",  "Viernes"   ,3.738, -0.04,  3.738,  3.751),
("2024-08-15",  "Jueves ",3.739 ,-0.03, 3.738,  3.751),
("2024-08-14",  "Miércoles",    3.740,  -0.15,  3.722,3.752),
("2024-08-13",  "Martes"    ,3.746, 0.03,   3.728,  3.746),
("2024-08-12",  "Lunes" ,3.745  ,0.36,  3.724,  3.745),
("2024-08-09",  "Viernes",  3.731,  0.15    ,3.726, 3.743),
("2024-08-08",  "Jueves",   3.726   ,0.06,  3.720,  3.739),
("2024-08-07",  "Miércoles" ,3.723  ,0.07,  3.717,  3.723),
("2024-08-06",  "Martes",   3.721   ,-0.49, 3.721,  3.739),
("2024-08-05",  "Lunes" ,3.739  ,0.00,  3.709,  3.739),
("2024-08-02",  "Viernes",  3.739,  -0.11,  3.735,  3.743),
("2024-08-01", "jueves" ,3.743, 0.20,   3.733,  3.743),
("2024-07-31",  "Miércoles",    3.736,  -0.05,  3.727,  3.744),
("2024-07-30",  "Martes ",3.738 ,0.02,  3.737,  3.743),
("2024-07-29",  "Lunes",    3.737   ,-0.54, 3.737,  3.759)

    
    
    # Añadir el resto de los datos proporcionados...
]

# Simulación de los próximos 15 días
dias_simulados = 15

# Inicializar el precio de cierre del último día de los datos históricos
precio_inicial = datos_dolar[-1][2]

# Función para calcular la variación diaria basada en los datos históricos
def generar_variacion_diaria(datos):
    variaciones = [dato[3] for dato in datos]  # Extraer las variaciones %
    return random.choice(variaciones)  # Elegir una variación aleatoria de los datos históricos

# Generar la simulación de precios para los próximos 15 días
simulacion_dolar = []

for dia in range(dias_simulados):
    variacion = generar_variacion_diaria(datos_dolar)  # Obtener una variación aleatoria
    precio_cierre = precio_inicial * (1 + variacion / 100)  # Calcular el precio de cierre con la variación
    precio_minimo = precio_cierre * random.uniform(0.99, 1.00)  # Suponer que el precio mínimo es un 0.99-1.00 del cierre
    precio_maximo = precio_cierre * random.uniform(1.00, 1.01)  # Suponer que el precio máximo es un 1.00-1.01 del cierre
    
    # Añadir el día simulado a la lista
    simulacion_dolar.append((f"Día {dia+1}", round(precio_cierre, 3), round(precio_minimo, 3), round(precio_maximo, 3), round(variacion, 2)))
    
    # Actualizar el precio de cierre para el siguiente día
    precio_inicial = precio_cierre

# Mostrar los resultados de la simulación
for dia, precio_cierre, precio_minimo, precio_maximo, variacion in simulacion_dolar:
    print(f"{dia}: Precio de cierre = {precio_cierre} | Mínimo = {precio_minimo} | Máximo = {precio_maximo} | Variación = {variacion}%")

