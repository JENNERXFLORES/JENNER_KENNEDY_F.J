lanterior=float(input("\ningrese lectura anterior en kiloWats :"))
lpresente=float(input("ingrese lectura presente en kilowaks :"))
usuario=input("ingrese tipo de usuario__ 1 2 3 4 :")
print("---------------------------------------------")
kilowats=lpresente-lanterior
if usuario=="1":
    tarifa=2.2
    print("\ntipo   tarifa  kilowats Switch ")
    for tipo in range(2):
       switch=kilowats*tarifa
    print("%3d  %5.1f  %6.1f %8.1f"%(tipo,tarifa, kilowats,switch))
elif usuario=="2":
    tarifa=2.8
    print("\ntipo   tarifa  kilowats Switch ")
    for tipo in range(1,3):
       switch=kilowats*tarifa
    print("%3d  %5.1f  %6.1f %8.1f"%(tipo,tarifa, kilowats,switch))

elif usuario=="3":
    tarifa=3.4
    print("\ntipo   tarifa  kilowats Switch ")
    for tipo in range(2,4):
       switch=kilowats*tarifa
    print("%3d  %5.1f  %6.1f %8.1f"%(tipo,tarifa, kilowats,switch))
else:
    tarifa=3.9
    print("\ntipo   tarifa  kilowats Switch ")
    for tipo in range(3,5):
       switch=kilowats*tarifa
    print("%3d  %5.1f  %6.1f %8.1f"%(tipo,tarifa, kilowats,switch))
    