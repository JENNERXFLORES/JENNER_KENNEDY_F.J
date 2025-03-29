#7
cantidad=float(input("ingrese cantidad de dinero a repartir:"))
edad1=int(input("ingrese edad de la primera persona :"))
edad2=int(input("ingrese edad de la segunda persona :"))
edad3=int(input("ingrese edad  de la tercera persona :"))

persona1=(edad1*cantidad)/(edad1+edad2+edad3)
persona2=(edad2*cantidad)/(edad1+edad2+edad3)
persona3=(edad3*cantidad)/(edad1+edad2+edad3)
print("\nmonto de la persona 1 :",persona1)
print("\nmonto de la persona 2 :",persona2)
print("\nmonto de la persona 3 :",persona3)
#comprobacion de monto.
mot_original=persona1+persona2+persona3
print("\nmonto original:",mot_original)