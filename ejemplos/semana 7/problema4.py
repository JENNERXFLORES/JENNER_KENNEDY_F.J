pcamisa=float(input("Precio de la camisa:"))
cant=int(input("Cantidad de unidades de camisas:"))

impcom=pcamisa*cant
desc1= impcom*0.07
aplicdesc1=impcom-desc1
desc2= aplicdesc1*0.07
desctotal=desc1+desc2

imppagar=impcom-desctotal
print("El importe de compra es S/.",impcom)
print("El importe del primer descuento es S/.", round(desc1,2))
print("El importe del segundo descuento es S/.",round(desc2,2))
print("El importe del descuento total es S/.",round(desctotal,2))
print("El importe a pagar es S/.",imppagar)
