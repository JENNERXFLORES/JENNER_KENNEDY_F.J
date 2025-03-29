#DESARROLLO 3:
import random
zona=["","sur","centro","Norte"]
porc=[0,0.08,0.12,0.14]
vendedor=int(input("# de vendedor :"))
c1=0; c2=0;c3=0  
sm1=0; sm2=0;sm3=0 
print("vend.  zona           ventas       comicion ")
for n in range(1,vendedor+1):
    nse=random.randint(1,3)
    venta=random.randint(500,4000)
    comision=venta*porc[nse]
    if nse==1:
    
        c1=c1+1  ; sm1=sm1+comision
    elif nse==2:
        c2=c2+1 ; sm2=sm2+comision
    else:
        c3=c3+1; sm3=sm3+comision
    print("%-5d  %-15s  %-5d   %10.1f"%(n,zona[nse],venta,comision)) 
print("------------------------------------------------------------------")
print(" zona %-15s  cantidad %4d   Comision total %8.1f"%(zona[1],c1,sm1))
print(" zona %-15s  cantidad %4d   Comision total %8.1f"%(zona[2],c2,sm2))
print(" zona %-15s  cantidad %4d   Comision total %8.1f"%(zona[3],c3,sm3))