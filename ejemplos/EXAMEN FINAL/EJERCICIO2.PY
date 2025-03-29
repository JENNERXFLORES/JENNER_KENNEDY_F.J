#DESARROLLO 2:
cont=0
sum=0
for x in range (10+1,100):
    if x%5==0:
        print(x,end=",")
        cont=cont+1
        sum=sum+x

print("\n\nla suma de los digitos comprendidos entre 10 y 99 es :",sum)
print("\nlos numeros que intervienen son :",cont)