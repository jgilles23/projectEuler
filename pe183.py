# %%
import math



total = 0
for N in range(5, 10000 + 1):
    k_low = int(N/math.e)
    k_high = k_low + 1
    if k_low*math.log(N/k_low) < k_high*math.log(N/k_high):
        k = k_high
    else:
        k = k_low
    g = math.gcd(N, k)
    k_new = k // g
    while True:
        h = math.gcd(k_new, 10)
        if h == 1:
            break
        k_new = k_new // h
    if k_new == 1:
        #Terminating decimal
        total -= N
    else:
        #Non-terminating decimal
        total += N
print("ans", total)

# %%
