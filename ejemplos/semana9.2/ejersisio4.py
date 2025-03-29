nbolo=int(input("escribe el numero de bolo: "))
if nbolo>0 and nbolo<21:
    print(" te llevas un lapicero")
elif nbolo<41:
    print("te llevas un cuaderno de 100 hojas")
elif nbolo<61:
    print("te llevas una caja de plumones") 
elif nbolo<81:
    print("te llevas un cuaderno espiral")
elif nbolo<99:
    print ("te llevas una agenda")
elif nbolo==100:
    print("te llevas una mochila")
else:
    print("ninguno")
