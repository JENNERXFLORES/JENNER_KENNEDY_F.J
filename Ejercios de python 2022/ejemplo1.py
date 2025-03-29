uni=int(input("unidades a comprar:"))
if uni>=1 and uni<=10:
    puni=25
elif uni<=18:
    puni=23.5
elif uni<=25:
    puni=21.4
else:
    puni=20.3 
pago=puni*uni
print("precio unitario :",puni)
print("pago total :",pago)
