#Project Euler 194
from copy import deepcopy
import math


#GRAPH UNIT ARCHITYPES
#top left = 0
#top right = 1
    #bottom right = 0
        #bottom left = 1
        #bottom left = 2
    #bottom right = 2
        #bottom left = 1
        #bottom left = 3

class Graph:
    def __init__(self, colorsAvaliable:int):
        self.colorsAvalaible = colorsAvaliable
        self.colorCount = 0
        self.permutations = 1
        self.nodeEdges = []
        self.nodeColors = []

    def __repr__(self):
        #Returning printing string for debugging
        s = f"<perms: {self.permutations}, colors: {self.colorCount} of {self.colorsAvalaible}, nodes: {len(self.nodeColors)}:{self.nodeColors}>"
        return s
    
    def addNode(self, edges: list):
        #Add a node to the graph, split the graph into however many graphs are required and return that list of graphs
        newGraphs = []
        for color in range(self.colorCount):
            #Use an existing color where possible
            for edge in edges:
                #check if color matches an existing edge
                if self.nodeColors[edge] == color:
                    break
            else:
                #For case does not break
                G = deepcopy(self)
                G.nodeColors.append(color)
                G.nodeEdges.append(edges)
                newGraphs.append(G)
        #Use a new color if possible
        if self.colorCount < self.colorsAvalaible:
            color = self.colorCount
            G = deepcopy(self)
            G.colorCount += 1
            G.nodeColors.append(color)
            G.nodeEdges.append(edges)
            G.permutations = (G.colorsAvalaible - color)*G.permutations
            newGraphs.append(G)
        return newGraphs


def stepGraphConstruction(graphs, node, edges):
    #Returns new list of graphs after a node has been added at each of the specificed edges
    newGraphs = []
    for graph in graphs:
        newGraphs += graph.addNode(edges)
    # for graph in newGraphs:
    #     print("node:", node, "|", graph)
    return newGraphs




#Calculate the number of type A and type B permutations
#For Added A's or B's to the graph. The base A or B will have an extra N*(N-1) permutations avaliable
def calcPermutations(colorsAvaliable, typeAFlag):
    graphs = [Graph(colorsAvaliable)]
    graphs = stepGraphConstruction(graphs, 0, []) #0
    graphs = stepGraphConstruction(graphs, 1, [0]) #1
    graphs = stepGraphConstruction(graphs, 2, [1]) #2
    if typeAFlag:
        graphs = stepGraphConstruction(graphs, 3, [0, 2]) #3 (changes based on type A: [0, 2] / B: [0])
    else:
        graphs = stepGraphConstruction(graphs, 3, [0]) #3 (changes based on type A: [0, 2] / B: [0])
    graphs = stepGraphConstruction(graphs, 4, [0, 1]) #4
    graphs = stepGraphConstruction(graphs, 5, [4]) #5
    graphs = stepGraphConstruction(graphs, 6, [2, 3, 5]) #6
    typePermutations = 0
    for graph in graphs:
        typePermutations += graph.permutations
    typePermutations = typePermutations // colorsAvaliable // (colorsAvaliable - 1)
    print("permutations:", typePermutations)
    return typePermutations



def coloredConfigurations(a,b,c, m):
    #a: number of type A, b: number of type B, c: number of colors avaliable
    #m: muodulus of the calculation
    #Create the graphs and print
    permutationsA = calcPermutations(c, True) % m
    permutationsB = calcPermutations(c, False) % m
    N = c*(c-1)
    for _ in range(a):
        N = (N*permutationsA)%m
    for _ in range(b):
        N = (N*permutationsB)%m
    #Update for the number of permutations
    N = (N*math.comb(a+b, a))%m
    return N


#AABB ABAB ABBA *inverse = 6
a, b, c = [25,75,1984]
M = 10**8
print("coloredConfigurations", coloredConfigurations(a, b, c, M))