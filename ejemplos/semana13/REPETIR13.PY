mes=[0,6,12,18]
interes1=[0,20,30,40,]
tipo=int(input("ingrese los mes conveniente 1=6 2=12 2=18:"))
precio=float(input("ingrese precio :"))
interes=precio*interes1[tipo]/100
saldo=interes+precio
cuota=saldo/mes[tipo]
print("mes  cuota m..  saldo ")
for n in range(1,mes[tipo]+1):
    saldo=saldo-cuota
    print("%-5d  %-8.1f  %-10.1f"%(n,cuota,saldo))
    