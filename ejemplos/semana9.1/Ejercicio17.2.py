#Una papelera puesto en oferta la venta de papel Bond en paquetes de medio millar de acuerdo con los siguientes criterios:
#- Para compras menores iguales a 20 se paga el precio normal.
#- Para compras mayores a 20 paquetes, por los primeros 20 paquetes se paga el precio normal, por los paquetes que exceden de 20 solo se paga el 85% del precio normal.
#Adicionalmente para compras de más de 50 paquetes el cliente recibe 2 paquetes adicionales.
#Determina el importe a pagar y la cantidad total de paquetes que recibirá el cliente.
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