max=0
for x in range(5):
    num=int(input("ingrese numero:"))
    if num>max:
        max=num
print("el mayor es", max)


min=9999
for x in range(5):
    num=int(input("ingrese numero:"))
    if num<min:
        min=num
print("el minimo es", min)