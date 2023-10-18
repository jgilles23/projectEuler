# %%
import numpy as np

total_members = 10**6

M = 2**10
def lagged_fib_generator():
    S_mod = [0]*M
    for k in range(1, 56):
        s = (100003 - 200003*k + 300007*k**3) % total_members
        S_mod[k] = s
        yield s
    while True:
        k += 1
        s = (S_mod[(k - 24) % M] + S_mod[(k - 55) % M]) % total_members
        S_mod[k % M] = s
        yield s



# %%

PM_member = 524287
PM_fraction = 0.99

# group_by_member = np.arange(total_members)
# size_by_group = np.full(total_members, 1)
# members_by_group = {}
# largest_group = -1
# largest_group_cutoff = 100

# generator = lagged_fib_generator()
# call_count = 0
# previous_PM_group_size = 0
# remaining_singles = total_members
# while size_by_group[group_by_member[PM_member]] < PM_fraction*total_members:
#     if size_by_group[group_by_member[PM_member]] > previous_PM_group_size:
#         print("PM group size:", size_by_group[group_by_member[PM_member]])
#         previous_PM_group_size = size_by_group[group_by_member[PM_member]]
#     member_0 = generator.__next__()
#     member_1 = generator.__next__()
#     if member_0 == member_1:
#         #Misdial
#         continue
#     call_count += 1
#     group_0 = group_by_member[member_0]
#     group_1 = group_by_member[member_1]
#     if group_0 == group_1:
#         #If already in the same group, nothing changes
#         continue
#     # Get a continuous order where size(group_1) > size(group_0), always
#     if size_by_group[group_0] > size_by_group[group_1]:
#         member_0, member_1 = member_1, member_0
#         group_0, group_1 = group_1, group_0
#     #Check if either of the members can be simply added
#     if size_by_group[group_0] == 1:
#         if group_1 == largest_group:
#             # Add to largest group, do not need a special index
#             pass
#         elif size_by_group[group_1] == 1:
#             # Start a members by group
#             members_by_group[group_1] = [member_0, member_1]
#         else:
#             #Add to the members group
#             members_by_group[group_1].append(member_0)
#         size_by_group[group_0] = 0
#         group_by_member[member_0] = group_1
#         size_by_group[group_1] += 1
#         remaining_singles -= 1
#     else:
#         #Need to make multiple changes, iterate through the entire list
#         size_by_group[group_1] += size_by_group[group_0]
#         size_by_group[group_0] = 0
#         group_by_member[members_by_group[group_0]] = group_1
#         if member_1 != largest_group:
#             if largest_group == -1 and size_by_group[group_1] > largest_group_cutoff:
#                 largest_group = group_1
#             else:
#                 members_by_group[group_1].extend(members_by_group[group_0])
#         members_by_group.pop(group_0)
#         print("Merged group size:", size_by_group[group_1], "remaining singles:", remaining_singles)
# print("ans:", call_count)

# %% Try with multiple re-direction method
group_by_member = np.arange(total_members)
size_by_group = np.full(total_members, 1)
generator = lagged_fib_generator()
call_count = 0
remaining_singles = total_members

def get_group(member):
    while member != (group := group_by_member[member]):
        member = group
    return group

while size_by_group[group_by_member[PM_member]] < PM_fraction*total_members:
    member_0 = generator.__next__()
    member_1 = generator.__next__()
    if member_0 == member_1:
        #Misdial
        continue
    call_count += 1
    group_0 = get_group(member_0)
    group_1 = get_group(member_1)
    if group_0 == group_1:
        #If already in the same group, nothing changes
        continue
    # Get a continuous order where size(group_1) > size(group_0), always
    if size_by_group[group_0] > size_by_group[group_1]:
        member_0, member_1 = member_1, member_0
        group_0, group_1 = group_1, group_0
    #Remove singles
    if size_by_group[group_0] == 1:
        remaining_singles -= 1
        if remaining_singles % 10000 == 0:
             print("Merged group size:", size_by_group[group_1] + size_by_group[group_0], "remaining singles:", remaining_singles)
    # Re-direct group size
    size_by_group[group_1] += size_by_group[group_0]
    size_by_group[group_0] = 0
    group_by_member[group_0] = group_1
print("ans", call_count)