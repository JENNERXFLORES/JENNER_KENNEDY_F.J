#Desarrollo
monto=int(input("ingrese el monto :"))
if monto>100:
    descuento=monto*0.1
    mp=monto-descuento
else:
    descuento=monto*0.2
    mp=monto-descuento
print("descuento considerado")
print(descuento)
print("monto presente")
print(mp)
