a=int(input("lado1:"))
b=int(input("lado2:"))
c=int(input("lado3:"))
if a+b>c and b+c>a and a+c>b:
    if a==b and b==c and c==a:
        print("equilatero")
    elif a!=b and b!=c != c!=a:
        print("escaleno")
    else:
        print("isosceles")
else:
    print("no forma triangulo")
