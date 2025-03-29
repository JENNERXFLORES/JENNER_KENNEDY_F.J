def calendario(monto, meses):
    interes=0.10*meses*monto
    saldo=interes+monto
    cuota=saldo/meses
    print("interes  ",interes)
    print("mes   cuota    saldo")
    for m in range(1,meses+1):
        saldo=saldo-cuota
        print("%4d  %10.f    %10.1f"%(m,cuota,saldo))
#el principal
calendario(4000,6)
print("=========")
calendario(3500,10)
