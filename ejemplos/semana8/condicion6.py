#DESARROLLO
Sex=input("Ingrese su sexo, Femenino=F Masculino=M:")
edad=int(input("Ingrese su edad:"))

if Sex=="Femenino" or Sex=="F":
   if edad<23:
       Sexo="FA"
   else:
       Sexo="FB"

if Sex=="Masculino" or Sex=="M":
   if edad<25:
       Sexo="MA"
   else:
       Sexo="MB"

print("A la categoria que pertecene es ", Sexo)