print("numero   nombre    raizCd   RaizCubica")
cad=["juan","maria","fernando","gabriel","luis"]
con=0
for x in range(8,13):
    raiz=x**(1/2)
    cb= x**(1/3)
   # print(x, " ",cad[con]," ",raiz)
    print("%8d  %-10s  %10.2f  %10.2f  "%(x,cad[con],raiz,cb))
    con=con+1
