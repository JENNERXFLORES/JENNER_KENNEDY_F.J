lanterior=float(input("ingrese lectura anterior en kiloWats :"))
lpresente=float(input("ingrese lectura presente en kilowaks :"))
lista=[0,2.2,2.8,3.4,3.9]
tipo=int(input("ingrese tipo de usuario 1-4 :"))
kilowats=lpresente-lanterior
pago=kilowats*lista[tipo]
print("switch=",pago)
print("kilowats=",kilowats)