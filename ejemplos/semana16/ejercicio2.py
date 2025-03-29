lista=[[],[6,25],[12,40],[18,60],[24,80]]
tipo=int(input("ingrese tipo de venta 1-4:"))
precio=float(input("ingrese precio :"))
x=lista[tipo]
print("tipo  %d meses %d interes porc %d"%(tipo,x[0],x[1]))
interes=precio*x[1]/100
saldo=interes+precio
cuota=saldo/x[0]
print("interes a pagar ",interes)
print("saldo    ",saldo)
print("cuota %5.2f"%(cuota))
