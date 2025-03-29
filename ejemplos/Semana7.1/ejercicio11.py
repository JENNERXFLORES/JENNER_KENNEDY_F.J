
velocidad1 = float(input("ingrese la velocidad del coche 1 (km/h):"))
velocidad2 = float(input("ingrese la velocidad del coche 2 (km/h):"))
distancia = float(input("ingrese la distancia entre los coches (km):"))
tiempo = distancia / abs(velocidad1 - velocidad2)
tiempo = tiempo * 60
print("Lo alcanza en",tiempo,"minutos.")
