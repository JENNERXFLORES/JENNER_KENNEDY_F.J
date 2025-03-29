shextra=0
shnormal=0
spsem=0

horasw=1
res="si"
while res=="si":
    nombre=input("Ingrese el nombre del Operario: ")
    cat=input("Ingrese la categoria: ")
    horasw=float(input("Ingrese las horas trabajadas en la semana: "))
    if horasw>0:
        phnormal=float(input("Pago normal por hora: "))
        hextras=0
        if horasw>48:
            hextras=horasw-48
        hnormales=horasw
        if horasw>48:
            hnormales=48
        pnormal=hnormales*phnormal
        pextra=hextras*phnormal*1.50
        psemanal=pnormal+pextra
        print("-----------------------------------")
        print("   B O L E T A   D E   P A G O     ")
        print("-----------------------------------")
        print("OPERARIO         :  ",nombre)
        print("CATEGORIA        :  ",cat)
        print("HORAS TRABAJADAS :  ",horasw)
        print("PAGO X HORA      :  ",phnormal)
        print(f"HORAS EXTRAS     :   {hextras}\tS/. {round(pextra,2)}")
        print(f"HORAS NORMALES   :   {hnormales}\t\tS/. {round(pnormal,2)}")
        print(f"PAGO SEMANAL     :   \t\tS/. {psemanal}")
        print("-----------------------------------")
        res=input("desea continuar: ")
