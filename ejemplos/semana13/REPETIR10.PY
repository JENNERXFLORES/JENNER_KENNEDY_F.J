tipo=int(input("moneda 1=soles 2=dolares:"))
monto=float(input("ingrese monto:"))
meses=int(input("numero de meses:"))
#tabla de interes xmes
print("mes    interes      total")
for m in range(1,meses+1):
    if tipo==1:
        interes=0.02*monto*m 
    else:
        interes=0.01*monto*m 
    total=monto+interes
    print("%5d  %8.1f     %10.1f"%(m,interes,total))