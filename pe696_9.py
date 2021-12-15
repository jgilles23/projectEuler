


valid_towers = set()
def verify_tower(tower):
    if not all([t <= 4 for t in tower]):
        return False
    tower = tuple([t for t in tower if t > 0])
    if tower in valid_towers:
        return False
    else:
        valid_towers.add(tower)
        return True


def expand_tower(base, t_max, t=0):
    if t >= t_max:
        return
    #Add a sequence to the base
    tower = [0,0,0] + list(base) + [0,0,0]
    for i in range(len(tower) -3 ):
        tower[i] += 1
        tower[i+1] += 1
        tower[i+2] += 1
        if verify_tower(tower):
            expand_tower(tuple(tower), t_max, t+1)
        tower[i] -= 1
        tower[i+1] -= 1
        tower[i+2] -= 1
    for i in range(2,len(tower) - 5):
        tower[i] += 3
        if verify_tower(tower):
            expand_tower(tuple(tower), t_max, t+1)
        tower[i] -= 3


expand_tower([], t_max=5)
print(len(valid_towers))
#print(valid_towers)


