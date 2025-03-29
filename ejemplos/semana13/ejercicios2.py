import random
c1=1
for n in range (1,21):
    num=random.randint(100,300)
    if num<=1000:
        c1=c1+1
        comi=8
    elif num<=2000:
        comi=12
        c1=c1+1
    else:
        c1=c1+1
        comi=15
        
print("%5d  %8.1f   %10.1f"%(n,num,comi))
