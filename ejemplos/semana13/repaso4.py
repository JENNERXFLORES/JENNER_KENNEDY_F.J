#generar 50 numeros (1,200) , cuantos son impares y pares
import random
cp=0; ci=0
for n in range(1,51):
    num=random.randint(1,200)
    print(num,end=",")
    if num%2==0:
        cp=cp+1
    else:
        ci=ci+1
print("\n nueros de pares %d numeros de impares %d"%(cp,ci))
