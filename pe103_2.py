import numpy as np
import math

class Node:
    def __new__(cls, parent=None, n=None):
        # print("Add", n, "to", parent, " -> ", end="")
        if parent is None:
            #No parent, must be the empty set
            obj = object.__new__(cls)
            obj.sum = 0
            obj.max = 0
            obj.list = []
            obj.bin = 0b1
            print(obj)
            return obj
        #there is a parent check the binary
        #Check if the new sets are dis-joint
        new_bin = parent.bin << n
        if (new_bin & parent.bin) != 0:
            #Sets are not dis-joint
            # print("Sets not dis-joint")
            return "disjoint"
        #Passed checks, setup object
        obj = object.__new__(cls)
        obj.sum = parent.sum + n
        obj.max = n
        obj.list = parent.list.copy() + [n]
        obj.bin = new_bin ^ parent.bin
        #Check if the new set passes the length rule S(B) > S(C) if L(B) > L(C)
        #SLOW CHECK
        for i in range(1, int(math.ceil(len(obj.list)/2))):
            if sum(obj.list[0:i+1]) <= sum(obj.list[-i:]):
                # print("Length check fail", "i",i, sum(obj.list[0:i+1]), sum(obj.list[-i:]))
                return "length"
        #Return the completed object
        # print(obj)
        return obj
    def __repr__(self):
        s = str(self.sum) + " " + str(self.list)
        return s



N = 7 # Desired L(A)

best_node = Node()
best_node.sum = 10**6
new_stack = [Node()]

i = 0
while len(new_stack) > 0 :
    i += 1
    #Sort existing stack by reverse length then sum
    stack = new_stack
    new_stack = []
    stack.sort(key=lambda x: (-1*len(x.list),x.sum))
    print(i, "STACK LENGTH", len(stack))
    #Iterate through the list
    for node in stack:
        # print("  > ", end="")
        new_node = Node(node, i)
        if new_node == "disjoint":
            new_stack.append(node)
            continue
        elif new_node == "length":
            #Add nothing to the new stack
            continue
        elif new_node.sum + i*(N - len(new_node.list)) >= best_node.sum:
            #Sum too large
            continue
        #Passed checks
        new_stack.append(node)
        if len(new_node.list) < N:
            new_stack.append(new_node)
        if len(new_node.list) == N:
            print("*** FOUND ANSWER", new_node)
            if new_node.sum < best_node.sum:
                best_node = new_node
print("ANSWER", best_node)
print("".join(str(x) for x in best_node.list))
