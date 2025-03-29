#promedio de talla
smt=0
cuenta=0
talla=1
while talla>0:
    talla=float(input("ingrese talla 0=finaliza :"))
    if talla>0:
        smt=smt+talla
        cuenta= cuenta+1
#fin while
prom=smt/cuenta
print("# de personas ",cuenta)
print("promedio de la talla :",prom)

