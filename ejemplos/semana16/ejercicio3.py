tipo=int(input("ingrese tipo de venta 1-4:"))
precio=float(input("ingrese precio :"))
if tipo==1:
    mes=6; pint=25
if tipo==2:
    mes=12; pint=40
if tipo==3:
    mes=18; pint=60
if tipo==4:
    mes=24; pint=80
interes=precio*pint/100
saldo=interes+precio
cuota=saldo/mes
print("interes a pagar ",interes)
print("saldo    ",saldo)
print("cuota %5.2f"%(cuota))
