lugar=["","1-ancash","2-tacna","3-cuzco","4-arequipa","5-piura"]
costo=[0,80,90,120,100,85]
print(lugar)
num=int(input("ingrese lugar :"))
npasajes=int(input("numero de pasajes :"))
importe=npasajes*costo[num]
print("lugar destino ", lugar[num])
print("costo del pasaje :", costo[num])
print("importe a pagar :",importe)