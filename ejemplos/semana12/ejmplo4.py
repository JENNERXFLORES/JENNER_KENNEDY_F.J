import random
nomsec=["","produccion","almacen","limpieza"]
tarifa=[0,18.5,17,16.5]
c1=0; c2=0;c3=0  #contadores
sm1=0; sm2=0;sm3=0 #acumuladores
print("  nro  seccion            horas      pago ")
for n in range(1,26):
    nse=random.randint(1,3)
    hora=random.randint(10,50)
    pago=hora*tarifa[nse]
    if nse==1:
       # pago=hora*18.5  ; nomsec="Produccion"
        c1=c1+1  ; sm1=sm1+pago
    elif nse==2:
        c2=c2+1 ; sm2=sm2+pago
    else:
        c3=c3+1; sm3=sm3+pago
    print("%5d  %-15s  %5d   %10.1f"%(n,nomsec[nse],hora,pago)) 
print(" seccion %-15s  cantidad %4d  Total Pago %8.1f"%(nomsec[1],c1,sm1))
print(" seccion %-15s  cantidad %4d  Total Pago %8.1f"%(nomsec[2],c2,sm2))
print(" seccion %-15s  cantidad %4d  Total Pago %8.1f"%(nomsec[3],c3,sm3))