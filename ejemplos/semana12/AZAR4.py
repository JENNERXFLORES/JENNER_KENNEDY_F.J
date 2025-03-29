import random 
precio=float(input("precio de la compra :"))
bola=["blanco","rojo","verde","azul","negro"]
pdes=[10,12,8,11,5,0]
num=random.randint(0,5)
des=precio*pdes[num]/100
print(bola[num],"descuento",des)
