import random
c1=0; c2=0 ; c3=0
for n in range (1,51):
    num=random.randint(1,60)
    if num<25:
        c1=c1+1
    elif num<=50:
        c2=c2+1
    else:
        c3=c3+1
    print(num,end=",")
print("\n menores a 25:",c1)
print("de 25-50 : ",c2)
print("mayor a 50 :",c3)