
def recursive_count(current_length, max_length, count_lates, count_consecutive_absence):
    if count_lates > 1:
        return 0
    elif count_consecutive_absence >= 3:
        return 0
    elif current_length == max_length:
        return 1
    else:
        valid_count = 0
        #Late
        valid_count += recursive_count(current_length+1, max_length, count_lates+1, 0)
        #On Time
        valid_count += recursive_count(current_length+1, max_length, count_lates, 0)
        #Absent
        valid_count += recursive_count(current_length+1, max_length, count_lates, count_consecutive_absence+1)
        return valid_count

def add_layer(late_abscent_dict):
    new_dict = {}
    def add_to_dict(D, key, value):
        if key in D:
            D[key] += value
        else:
            D[key] = value
    for late_count, absence_count in late_abscent_dict:
        value = late_abscent_dict[(late_count, absence_count)]
        #Late
        if late_count == 0:
            add_to_dict(new_dict, (late_count+1, 0),  value)
        #On Time
        add_to_dict(new_dict, (late_count, 0), value)
        #Absent
        if absence_count < 2:
            add_to_dict(new_dict, (late_count, absence_count+1), value)
    return new_dict

L = 30
# print("ans", recursive_count(0, L, 0, 0))

late_abscent_dict = {(0,0):1}
for n in range(L):
    late_abscent_dict = add_layer(late_abscent_dict)
print(late_abscent_dict)
print("ans", sum(late_abscent_dict.values()))
