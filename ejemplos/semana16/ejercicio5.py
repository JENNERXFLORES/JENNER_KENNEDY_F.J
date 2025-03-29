origen=input("N=nacional I=importado:").upper()
sexo=input("F=femenino M=masculino:").upper()
talla=input("L=large, M=medium, S=small :").upper()
precio=float(input("ingrese monto:"))
if origen=="N":
    if sexo=="M":
        if talla=="L":
            des=0.15*precio
        elif talla=="M":
            des=0.12*precio
        else:
            des=0.10*precio
    else: #femenino
        if talla=="L":
            des=0.20*precio
        elif talla=="M":
            des=0.17*precio
        else:
            des=0.15*precio
else: #origen importado
     if sexo=="M":
        if talla=="L":
            des=0.10*precio
        elif talla=="M":
            des=0.07*precio
        else:
            des=0.05*precio
     else: #femenino
        if talla=="L":
            des=0.12*precio
        elif talla=="M":
            des=0.09*precio
        else:
            des=0.07*precio
tot=precio -des
print("descuento ",des)
print("total pago ",tot)
