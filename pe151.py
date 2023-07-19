import random

# Data sorage (A2, A3, A4, A5) number of pages remaining
# Index zero will be the second bath

batch_options_by_day = [{(1,1,1,1):1.0}]

for day in range(1, 14):
    batch_options = {}
    for option in batch_options_by_day[day-1]:
        #Count the number of choices
        pieces_of_paper = sum(option)
        for paper in range(4):
            if option[paper] == 0:
                continue
            # Paper exisits 
            new_option = [a for a in option] #Copy
            new_option[paper] -= 1
            # Add 1 to subsequent options
            for i in range(paper+1, 4):
                new_option[i] += 1
            # Re-tupalize the option for lookup
            new_option = tuple(new_option)
            if new_option in batch_options:
                batch_options[new_option] += batch_options_by_day[day-1][option]*option[paper]/pieces_of_paper
            else:
                batch_options[new_option] = batch_options_by_day[day-1][option]*option[paper]/pieces_of_paper
    batch_options_by_day.append(batch_options)

print("Daily options:")
for x in batch_options_by_day:
    print(x)

print("Daily Expected Value:")
# Iterate through the daily options and determine how many are dealing with a single piece of paper
single_sheet_by_day = []
for batch_options in batch_options_by_day:
    s = 0.0
    for option in batch_options:
        if sum(option) == 1:
            s += batch_options[option]
    single_sheet_by_day.append(s)

print(single_sheet_by_day)
A = sum(single_sheet_by_day)
print(A)
print("ans {:.6}".format(A))

# # Validate with simulation - SIMULATION IS FLAWED
# N = 1 + 10**5
# single_finds_by_day = [0 for _ in range(14)]
# for n in range(N):
#     envelope = [1,1,1,1]
#     for day in range(1,14):
#         r = random.randrange(0,4)
#         while envelope[r] == 0:
#             r = random.randrange(0,4)
#         envelope[r] -= 1
#         for i in range(r+1, 4):
#             envelope[i] += 1
#         #Count if the new envelope has singles
#         if sum(envelope) == 1:
#             single_finds_by_day[day] += 1
# single_finds_by_day = [x/N for x in single_finds_by_day]
# print(single_finds_by_day)
# print("EV:", sum(single_finds_by_day))
# pass       
