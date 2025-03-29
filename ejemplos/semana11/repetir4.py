nums=[]
num=int(input("Ingrese el numero del cual desea generar los numeros inferiores a el: "))
for n in range(0,num):
    nums.append(n)
nums.reverse()
print(nums)
