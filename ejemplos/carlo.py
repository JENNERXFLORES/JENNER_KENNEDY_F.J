
shextra=0;shnormal=0;resp="si"
spsem=0 ; op=0 ; ac1=0; ac2=0;ac3=0


while resp=="si":
    op=op+1
    nombre=input("\nIngrese el nombre del Operario %d: "%(op))
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
        ac1=ac1+hextras
        ac2=ac2+hnormales
        ac3=ac3+psemanal 
        resp=input("desea continuar si/no: ").lower()
thextras=ac1
thnormales=ac2
tpsemanal=ac3
print("\nTOTAL DE HORAS EXTRAS  :",thextras)
print("TOTAL DE HORAS NORMALES :",thnormales)
print("TOTAL DE PAGO SEMANAL ",tpsemanal)
print("------------------------------------")
