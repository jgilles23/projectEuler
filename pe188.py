N = 10**8

power = 1855
base = 1777
for k in range(1855):
    power = pow(base, power, N)
print("ans", power)

