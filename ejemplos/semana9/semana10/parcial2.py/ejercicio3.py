dis=float(input("Ingrese distancia recorrida:"))
if dis<=300:
    tari=250
elif dis<=1000:
    tarifba=250
    disextra=dis-300
    tarifex=disextra*30
    
    tari=tarifba+tarifex
else:
    tarifba=250
    disextra=dis-1000

    disextra2=1000-300
    
    tarifba2=disextra*20
    tarifba3=disextra2*30

    tari=tarifba+tarifba2+tarifba3

print("El monto que pagará el cliente es: S/.",tari)