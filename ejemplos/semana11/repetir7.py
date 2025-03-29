num=int(input("\n numero :"))
factorial=1
if  num!=0:
    for n in range(1,num+1):
        factorial=factorial*n
print("factorial de %d  es %d"%(num,factorial))