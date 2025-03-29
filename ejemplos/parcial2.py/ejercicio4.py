total=float(input("compra total :"))
colordb=input("ingrese B=blanco  V=verde A=amarillo  Z=azul R=roja :")
if colordb=="A" or colordb=="a":
    des=total*0.75
elif colordb=="V"  or colordb=="v":
     des=total*0.9
elif colordb=="Z"  or colordb=="z":
    des=total*0.5
elif colordb=="R"  or colordb=="r":
    des=total*0.1
else: 
    colordb=="B" or colordb=="b"
    des=0
       
pagofinal=total-des
print("color de la bolita :",colordb)
print("descuento :",des)
print("cantidad final que debe pagar por su compra :",pagofinal)
   

