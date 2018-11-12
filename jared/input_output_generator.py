import networkx
from random import shuffle
import random

def generate_input():
    generate_small_output()

def generate_large_input():
    f = open("../deliverable1/inputs/large/parameters.txt", "w")

    write_rowdy_group(f, 0, 100)
    write_rowdy_group(f, 100, 200)
    write_rowdy_group(f, 200, 300)
    write_rowdy_group(f, 300, 400)
    write_rowdy_group(f, 400, 500)

    f.close()

    G = networkx.Graph()
    for i in range(500):
        G.add_node(i)

    add_edges_within(G, 0, 100)
    add_edges_within(G, 100, 200)
    add_edges_within(G, 200, 300)
    add_edges_within(G, 300, 400)
    add_edges_within(G, 400, 500)

    G.add_edge(99, 100)
    G.add_edge(99, 101)
    G.add_edge(99, 102)
    G.add_edge(99, 103)

    G.add_edge(199, 200)
    G.add_edge(199, 201)
    G.add_edge(199, 202)
    G.add_edge(199, 203)

    networkx.write_gml(G, "../deliverable1/inputs/large/graph.gml")

def generate_medium_input():
    f = open("../deliverable1/inputs/medium/parameters.txt", "w")

    list = [i for i in range(1000)]
    shuffle(list)
    write_list(f, list[0:50])
    shuffle(list)
    write_list(f, list[0:50])
    shuffle(list)
    write_list(f, list[0:50])
    shuffle(list)
    write_list(f, list[0:50])
    shuffle(list)
    write_list(f, list[0:50])
    shuffle(list)
    write_list(f, list[0:50])
    shuffle(list)
    write_list(f, list[0:50])
    shuffle(list)
    write_list(f, list[0:50])
    shuffle(list)
    write_list(f, list[0:50])
    shuffle(list)
    write_list(f, list[0:50])
    shuffle(list)
    write_list(f, list[0:50])
    shuffle(list)
    write_list(f, list[0:50])
    shuffle(list)
    write_list(f, list[0:50])
    shuffle(list)
    write_list(f, list[0:50])
    shuffle(list)
    write_list(f, list[0:50])
    shuffle(list)
    write_list(f, list[0:50])
    shuffle(list)
    write_list(f, list[0:50])
    shuffle(list)
    write_list(f, list[0:50])
    shuffle(list)
    write_list(f, list[0:50])
    shuffle(list)
    write_list(f, list[0:50])

    f.close()

    G = networkx.Graph()
    for i in range(500):
        G.add_node(i)

    for i in range(125000):
        x = random.randint(0, 500)
        y = random.randint(0, 500)
        if (x != y and not G.has_edge(x, y) and not G.has_edge(y, x)):
            G.add_edge(x, y)


    networkx.write_gml(G, "../deliverable1/inputs/medium/graph.gml")

def generate_medium_output():
    f = open("../deliverable1/outputs/medium.out", "w")

    list = [i for i in range(500)]
    shuffle(list)
    print(list)

    write_list(f, list[0:50])
    write_list(f, list[50:100])
    write_list(f, list[100:150])
    write_list(f, list[150:200])
    write_list(f, list[200:250])
    write_list(f, list[250:300])
    write_list(f, list[300:350])
    write_list(f, list[350:400])
    write_list(f, list[400:450])
    write_list(f, list[450:500])

    f.close()

def generate_small_output():
    f = open("../deliverable1/outputs/small.out", "w")

    list = [i for i in range(27)]
    shuffle(list)
    print(list)

    write_list(f, list[0:3])
    write_list(f, list[3:6])
    write_list(f, list[6:9])
    write_list(f, list[9:12])
    write_list(f, list[12:15])
    write_list(f, list[15:18])
    write_list(f, list[18:21])
    write_list(f, list[21:24])
    write_list(f, list[24:27])

    f.close()

def write_list(f, list):
    f.write("[")
    for i in list:
        f.write("'")
        f.write(str(i))
        f.write("'")
        f.write(",")
    f.write("]\n")

def generate_small_input():
    f = open("../deliverable1/inputs/small/parameters.txt", "w")

    write_rowdy_group(f, 0, 5)
    write_rowdy_group(f, 5, 10)
    write_rowdy_group(f, 10, 15)
    write_rowdy_group(f, 15, 20)
    write_rowdy_group(f, 20, 25)

    f.close()

    G = networkx.Graph()
    for i in range(27):
        G.add_node(i)

    add_friend_group(G, [1, 2, 3, 6])
    add_friend_group(G, [4, 5, 6])
    add_friend_group(G, [7, 8, 9])
    add_friend_group(G, [10, 11, 12])
    add_friend_group(G, [13, 14, 15])
    add_friend_group(G, [16, 17, 18])
    add_friend_group(G, [19, 20, 21])
    add_friend_group(G, [22, 23, 24])
    add_friend_group(G, [25, 26, 27])

    networkx.write_gml(G, "../deliverable1/inputs/small/graph.gml")

def add_friend_group(G, list):
    for i in list:
        for j in list:
            if (i != j):
                G.add_edge(i, j)



def add_edges_within(G, min, max):
    for i in range(min, max):
        for j in range(min, max):
            if (i != j):
                G.add_edge(i, j)

def write_rowdy_group(f, min, max):
    f.write("[")
    for i in range(min, max):
        f.write("'")
        f.write(str(i))
        f.write("'")
        f.write(",")
    f.write("]\n")

generate_input()