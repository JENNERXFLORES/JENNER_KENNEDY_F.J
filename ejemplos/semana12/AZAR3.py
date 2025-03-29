import random 
adivina=random.randint(1,60)
for intento in range(1,7):
    num=int(input("ingrese valor %d :"%intento))
    if num==adivina:
        print("acerto en el intento ",intento)  
        break
    if num>adivina:
        print("ingrese un numero menor a ",num)
    else:
        print("ingrese un numero mayor a ",num)
else:
    print("el numero fue  ",adivina)
