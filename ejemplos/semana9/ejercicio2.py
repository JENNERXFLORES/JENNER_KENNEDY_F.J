precio=float(input("ingrese precio :"))
tpago=input(" ingrese tipo 1 2 3 4  :")
print("------------------------------")
if tpago=="1":
    interes=0.25*precio
    saldo=precio+interes 
    cuota=saldo/6
    print("interes a pagar ",interes)
    print("------------------------------")
    print("   mes      cuota     saldo   ")
    for m in range(1,6+1):
        saldo=saldo-cuota
        print("%5d   %10.1f   %10.1f"%(m,cuota,saldo))

elif tpago=="2":
    interes=0.40*precio
    saldo=precio+interes 
    cuota=saldo/12
    print("interes a pagar ",interes)
    print("------------------------------")
    print("   mes      cuota     saldo   ")
    for m in range(1,12+1):
        saldo=saldo-cuota
        print("%5d   %10.1f   %10.1f"%(m,cuota,saldo))

elif tpago=="3":
    interes=0.60*precio
    saldo=precio+interes
    cuota=saldo/18
    print("interes a pagar ",interes)
    print("------------------------------")
    print("   mes      cuota     saldo   ")
    for m in range(1,18+1):
        saldo=saldo-cuota
        print("%5d   %10.1f   %10.1f"%(m,cuota,saldo))
else:
    interes=0.80*precio
    saldo=precio+interes 
    cuota=saldo/24
    print("interes a pagar ",interes)
    print("------------------------------")
    print("   mes      cuota     saldo   ")
    for m in range(1,24+1):
        saldo=saldo-cuota
        print("%5d   %10.1f   %10.1f"%(m,cuota,saldo))
