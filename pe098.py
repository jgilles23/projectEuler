with open("p098_words.txt", "r") as file:
    words = [word for word in file]
words = words[0].replace('"', "").split(",")
print("Num words", len(words))

#Find anagrams
anagram_counts = {}
for word in words:
    word_tuple = tuple(sorted(word))
    if word_tuple in anagram_counts:
        anagram_counts[word_tuple]["count"] += 1
        anagram_counts[word_tuple]["words"].append(word)
    else:
        anagram_counts[word_tuple] = {"count":1, "words":[word]}
lettercounts = {}
for word_tuple, d in anagram_counts.items():
    if d["count"] >= 2:
        lc = tuple(sorted([word_tuple.count(c) for c in set(word_tuple)]))
        if lc in lettercounts:
            lettercounts[lc].append(d["words"])
        else:
            lettercounts[lc] = [d["words"]]
print("Anagrams verified", len(lettercounts))
L = max([sum(lettercount) for lettercount in lettercounts])
print("Longest anagram", L)
#print(lettercounts)

#Generate all squares up to 10**10
digit_anagrams = {}
square = 0
i = 1
while square < 10**10:
    square = i**2
    square_str = str(square)
    square_hash = tuple([square_str.count(c) for c in set(square_str)])
    if square_hash in lettercounts:
        if square_hash in digit_anagrams:
            digit_anagrams[square_hash].append(square)
        else:
            digit_anagrams[square_hash] = [square]
    i += 1
digit_anagrams_verified = {}
for key, value in digit_anagrams.items():
    if len(value) >= 2:
        digit_anagrams_verified[key] = value
#print(digit_anagrams_verified)

keys_sorted = sorted([x for x in digit_anagrams_verified], key=lambda y: len(y), reverse=True)

for key_selection in keys_sorted:
    N = sorted(digit_anagrams_verified[key_selection], reverse=True)
    print(lettercounts[key_selection])
    for w0, w1 in lettercounts[key_selection]:
        for n in N:
            subs = {w0[i]:str(n)[i] for i in range(len(w0))}
            n1 = int("".join([subs[c] for c in w1]))
            if n1 in N:
                print("Found answer!", n, n1)
                break
        else:
            continue
        break
    else:
        print("No answer found for", key_selection)
        continue
    break