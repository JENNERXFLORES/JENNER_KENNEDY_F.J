hora=float(input("ingrese horas :"))
tarifa=float(input("pagox hora :"))
if hora>40:
    pago=40*tarifa+(hora-40)*tarifa*1.5
else:
    pago=hora*tarifa
#calcular su descuento
if pago>500:
    des=0.10*pago
else:
    des=0
total=pago-des
print("pago bruto :",pago)
print("descuento :",des)
print("total de pago :",total)