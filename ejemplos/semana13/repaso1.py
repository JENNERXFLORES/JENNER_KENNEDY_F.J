prestamo=float(input("ingrese prestamo:"))
meses=int(input("nro de meses pago:"))
#calculos
interes=prestamo*0.01*meses
saldo=interes+prestamo
cuota=saldo/meses
print("Interes a pagar :",interes)
print("mes     cuota      saldo")
for m in range(1,meses+1):
    saldo=saldo - cuota
    print("%5d  %8.1f    %10.1f"%(m,cuota,saldo))
