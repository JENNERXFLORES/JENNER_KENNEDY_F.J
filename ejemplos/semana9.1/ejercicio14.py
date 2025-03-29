#Desarrollo
h=int(input("ingresa la hora\n"))
m=int(input("ingresa minuto\n"))
s=int(input("ingresa segundo\n"))
if(h < 24 and m < 60 and s < 60):
 if(s < 59 and s >= 0):
  print(str(h)+"h "+str(m)+"m "+str(s+1)+"s")
 else:
  if(s==59):
   if(m==59):
    if(h==23):
     print("00h 00m 00s")
    else:
     print(str(h+1)+"h 00m 00s")
   else:
    print(str(h)+"h "+str(m+1)+"m 00s")        
else:
 print("Fuera de rango")