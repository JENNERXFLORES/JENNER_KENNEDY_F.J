cad1=["","C","CC","CCC","CD","D","DC","DCC","DCCC","CM"]
cad2=["","X","XX","XXX","XL","L","LX","LXX","LXXX","XC"]
cad3=["","I","II","III","IV","V","VI","VII","VIII","IX"]
num=int(input("ingrese un numero de 3 digitos:"))
cen=num//100     
res=num%100     
dec=res//10    
uni=res%10 
ct=cad1[cen]+cad2[dec]+cad3[uni]
print(num ," en romanos ",ct)
