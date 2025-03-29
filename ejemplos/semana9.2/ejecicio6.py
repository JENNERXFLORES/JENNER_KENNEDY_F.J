sexo=input("ingrese F=femenino M=masculino :")
edad=int(input("ingrese edad:"))
if sexo=="F" or sexo=="f":
    if edad<23:
        cat="FA"
    else:
        cat="FB"
else:
    if edad<25:
        cat="MA"
    else:
        cat="MB"        
    
print("la categoria ",cat)
