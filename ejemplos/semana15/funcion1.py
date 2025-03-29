lista=[]
for n in range(1,8):
    sueldo=float(input("persona %d :"%(n)))
    lista.append(sueldo)
lista.sort()
print("nro     sueldo    impuesto")
for n in range(1,8):
    if n>=1 and n<=3:
        imp=0.08*lista[n-1]
    else:
        imp=0.12*lista[n-1]
    print("%5d  %8d   %10.1f"%(n,lista[n-1],imp))
