serie1=3
print("primera serie")
for x in range(15):
    print(serie1,end=",")
    serie1=serie1+3
print("\nserie 2")
serie2=-5
for x in range(15):
    print(serie2,end=",")
    serie2=serie2-5
print("\n serie 3")
serie3=1
for x in range(15):
    print(serie3,end=",")
    serie3=serie3+2
print("\nserie 4")
serie4=5
for x in range(15):
    cd=serie4*serie4
    print(cd,end=",")
    serie4=serie4+1
print("\n serie5:")
serie5=1.5
for x in range(15):
    print("%3.1f"%serie5,end=",")
    serie5=serie5+0.1