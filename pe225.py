
# test_modulus = 27

# lookup = {}
# seq = [1, 1, 1]
# print ("1, 1, 1, ", end="")
# a, b, c = 1, 1, 1
# current_triple = (a, b, c)
# i = 0
# while current_triple not in lookup:
#     lookup[current_triple] = i
#     #Move to next
#     a, b, c = b, c, (a + b + c) % test_modulus
#     current_triple = (a, b, c)
#     seq.append(c)
#     print(f"{c}", end=", ")
#     i += 1

N = 124

count = 0
test_modulus = 1
while count < N:
    test_modulus += 2
    a, b, c = 1, 1, 3
    while not (a == 1 and b == 1 and c == 1):
        a, b, c = b, c, (a + b + c) % test_modulus
        if c == 0:
            break
    else:
        count += 1
        print(f"Solution {count}: {test_modulus}")
print("ans:", test_modulus)
