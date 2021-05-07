#Project euler problem #73 date 20210503
import math

D = 12000

count = 0
for d in range(1,D+1):
    n_min = int(d/3) + 1
    n_max = int(math.ceil(d/2)) 
    for n in range(n_min,n_max):
        if math.gcd(n,d) == 1:
            count += 1

print("ans",count)