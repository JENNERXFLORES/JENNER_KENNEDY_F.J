a=int(input("lado1:"))
b=int(input("lado2:"))
c=int(input("lado3:"))
if a+b>c or a+c>b or b+c>a:
    print("\nsi es un triangulo")
if a==b and b==c and c==a:
    print("\nEs un triagulo Equilatero")
elif a!=b and b!=c and c!=a:
    print("\nEs un triangulo Escaleno")
else:
    print("\nEs un triangulo Isoceles ")
