cen=num//100    
res=num%100     
dec=res//10    
uni=res%10     
if cen==1:
   cad1="C"
if cen==2:
   cad1="CC"
if cen==3:
   cad1="CCC"
if cen==4:
   cad1="CD"
if cen==5:
   cad1="D"
if cen==6:
   cad1="DC"
if cen==7:
   cad1="DCC"
if cen==8:
   cad1="DCCC"
if cen==9:
   cad1="CM"
#DECENA
if dec==1:
   cad2="X"
if dec==2:
   cad2="XX"
if dec==3:
   cad2="XXX"
if dec==4:
   cad2="XL"
if dec==5:
   cad2="L"
if dec==6:
   cad2="LX"
if dec==7:
   cad2="LXX"
if dec==8:
   cad2="LXXX"
if dec==9:
   cad2="XC"

#UNIDADES
if uni==1:
   cad3="I"
if uni==2:
   cad3="II"
if uni==3:
   cad3="III"
if uni==4:
   cad3="IV"
if uni==5:
   cad3="V"
if uni==6:
   cad3="VI"
if uni==7:
   cad3="VII"
if uni==8:
   cad2="VIII"
if uni==9:
   cad2="IX"
print ("romanos:",cad1+cad2+cad3)
