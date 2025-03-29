#el costo del pasaje varia de acuerdo al lugar
# lugar  precio
# ancash     80
#tacna      90
#cuzco      120
#arequipa   100
#piura      85
#ingrese el numero de pasajes obtener su importe

lugar=["","1-ancash","2-tacna","3-cuzco","4-arequipa","5-piura"]
costo=[0,80,90,120,100,85]
print(lugar)
num=int(input("ingrese lugar :"))
npas=int(input("numero de pasajes:"))
importe=npas*costo[num]
print("lugar destino ",lugar[num])
print("costo del pasaje :",costo[num])
print("importe a pagar :",importe)
