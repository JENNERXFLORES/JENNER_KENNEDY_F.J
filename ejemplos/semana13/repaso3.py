velocidad1 = float(input("ingrese la velocidad 1 (mts/s):"))
velocidad2 = float(input("ingrese la velocidad 2 (mts/s):"))
distancia = float(input("ingrese la distancia entre los dos (m):"))
tiempo = distancia / abs(velocidad1 - velocidad2)
print("tiempo   distA    DistB")
for t in range(2, tiempo+1):
    da=velocidad1*t
    db=velocidad2*t
    print("%5d   %8.1f   %8.1f"%(t,da,db))