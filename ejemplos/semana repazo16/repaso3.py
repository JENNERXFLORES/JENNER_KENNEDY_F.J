smp=0; con=0
resp="s"
while resp=="s":
    con=con+1
    curso=input("\n vendedor  %d:"%(con))
    nro=int(input("# de ventas realisadas :"))
    sm=0
    for n in range(1,nro+1):
        venta=int(input(" venta %d:"%(n)))
        sm=sm+venta
    comicion=sm*0.12
    smp=smp+comicion
    print("%s su comicion  %3.1f"%(sm,comicion))
    resp=input("otro vendedor s/n:").lower()
comiciont=smp
print("comicion total a pagar :%3.2f"%(comiciont))