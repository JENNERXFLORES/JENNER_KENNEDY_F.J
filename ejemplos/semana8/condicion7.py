#DESARROLLO
cantpaq=int(input("Cantidad de paquetes de Hoja Bond a vender:"))
precio=float(input("Precio de un paquete de Hoja Bond:"))
if cantpaq<=20:
    Import=cantpaq*precio
else:
    exceso=cantpaq - 20
    primeros20paq= 20*precio

    oferta=(precio*85)/100

    ofertaplic= exceso*oferta

    Import= primeros20paq+ofertaplic

    
    if cantpaq>50:
        cantpaq=cantpaq+2
    else: 
        cantpaq=cantpaq
print("El importe a pagar es de S/.",Import)
print("Total de paquetes que recibirá el cliente:", cantpaq)