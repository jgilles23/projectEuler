shots = [0] + [*range(1,21)] + [*range(2,41,2)] + [*range(3,61,3)] + [25, 50]
print(shots)

count = 0
max_score = 99

for i in range(len(shots)):
    for j in range(i, len(shots)):
        pre_score = shots[i] + shots[j]
        #If pre-score too high, will never double out under 100
        if pre_score > max_score - 2:
            #pre-score too high, will never get low enough
            # print(pre_score, "too high", max_score - 2)
            pass
        elif pre_score <= max_score - 50:
            print([shots[i], shots[j]], pre_score, "count 21", max_score - 50)
            count += 21 #double out on everything including double bulls
        elif pre_score <= max_score - 40:
            print([shots[i], shots[j]], pre_score, "count 20", max_score - 40)
            count += 20
        else:
            print([shots[i], shots[j]], pre_score, "count tbd", "...", (max_score - pre_score)//2)
            count += min((max_score - pre_score)//2, 20)

print("ans", count)

