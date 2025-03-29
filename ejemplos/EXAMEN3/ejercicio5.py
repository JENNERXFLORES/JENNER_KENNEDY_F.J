#DESARROLLO
#calendario de pagos
costodecarro=float(input("precio del auto: "))
años=int(input("nro años: "))
#calculos
interes=costodecarro*0.10*años
saldo=interes+costodecarro
cuotamensual=saldo/(años*12)
print("Interes a pagar: ", interes)
print("Años Cuota   Saldo")
for m in range(1,años+1):
    saldo=saldo-cuotamensual
    print("%5d  %8.1f   %10.1f"%(m,cuotamensual,saldo))