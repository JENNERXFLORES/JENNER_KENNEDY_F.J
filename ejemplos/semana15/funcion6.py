lista=[[100,"Juan Perez",2300],[101,"Ana Huacal",2500],
[102,"Luis Zapata",1800]]
def muestra():
    print("codigo   nombre            sueldo     afp")
    for x in lista:
        afp=x[2]*0.11
        print("%5d  %-15s  %8d  %10.1f"%(x[0],x[1],x[2],afp))

#principal
muestra()
