#ingrese sueldo si es mayor o igual a 2500 paga impuesto que es 8% a la diferencia con 2500
sueldo=float(input("ingrese sueldo:"))
if sueldo>=2500:
    des=(sueldo-2500)*0.08
else:  #implicitamente es sueldo<2500
    des=0
pago=sueldo-des
print("descuento :",des)
print("pago total :",pago)
