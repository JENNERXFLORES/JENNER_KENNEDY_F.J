precio=float(input("precio del auto:"))
anio=int(input("nro de años "))
interes=0.1*anio*precio 
saldo=precio+interes
cuota=saldo/(anio*12)
print("interes apagar ",interes)
print("mes     cuota       saldo")
meses=anio*12
for m in range(1,meses+1):
    saldo=saldo-cuota
    print("%5d   %10.1f   %10.1f"%(m,cuota,saldo))
