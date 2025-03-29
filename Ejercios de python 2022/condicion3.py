can=int(input("# de docenas :"))
predoc=float(input("preciox docena :"))

impc=can*predoc 
if can>=10:
    des=impc*0.15
else: # implicitamente can<10
    des=impc*0.11

pago=impc-des 
if pago>=200:
    obs=2*can
else:
    obs=0
print("importe de compra :",impc)
print("descuento    :",des)
print("importe a pagar :",pago)
print("# de lapiceros :",obs)
