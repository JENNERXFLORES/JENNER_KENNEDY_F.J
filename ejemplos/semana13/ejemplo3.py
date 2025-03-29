num=int(input("ingrese un numero :"))
sm=1
while num>0:
    res=num%10
    sm=sm*res
    num=num//10 # 5673//10 =567
print("la suma de sus digitos :",sm)