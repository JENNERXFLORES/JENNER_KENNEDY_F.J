turno=input("ingrese M=mañana N=Noche:")
cant=int(input("# de pasajes :"))
if turno=="M" or turno=="m":
    impc=37.5*cant 
else:
    impc=45*cant 

if cant>=15:
    des=0.08*impc
else:
    des=0.05*impc 

pago= impc- des 
if pago>200:
    obs=2*cant
else:
    obs=0
print("importe de compra :",impc)
print("descuento  :",des)
print("importe de pago :",pago)
print("# de caramelos ",obs)
