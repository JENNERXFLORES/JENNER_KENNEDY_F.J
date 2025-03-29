lista=[[201,"juan perez",12,18],[202,"martin diaz",18,19],[203,"cielo piggi",20,13]]
def muestra():
    print(" CODIGO    NOMBRE      EXP    EXF")
    for x in lista:
        print("%5d  %-15s  %8d  %10.1f"%(x[0],x[1],x[2],x[3]))
def ingreso():
    np=int(input("numero de personas a ingresar:"))
    for n in range(np):
        cod=int(input("ingrese codigo:"))
        nombre=input("ingrese nombre:")
        exp=int(input("ingrese exp:"))
        exf=int(input("ingrese exf:"))
        lista.append([cod,nombre,exp,exf])



ingreso()
muestra()
