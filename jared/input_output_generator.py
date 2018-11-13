import networkx
from random import shuffle
import random

def generate_input():
    generate_large_input()
    generate_large_output()

def generate_large_input():
    f = open("../deliverable1/inputs/large/parameters.txt", "w")

    list = [i for i in range(1000)]
    shuffle(list)
    write_list(f, list[0:100])
    shuffle(list)
    write_list(f, list[0:100])
    shuffle(list)
    write_list(f, list[0:100])
    shuffle(list)
    write_list(f, list[0:100])
    shuffle(list)
    write_list(f, list[0:100])
    shuffle(list)
    write_list(f, list[0:100])
    shuffle(list)
    write_list(f, list[0:100])
    shuffle(list)
    write_list(f, list[0:100])
    shuffle(list)
    write_list(f, list[0:100])
    shuffle(list)
    write_list(f, list[0:100])
    shuffle(list)
    write_list(f, list[0:100])
    shuffle(list)
    write_list(f, list[0:100])
    shuffle(list)
    write_list(f, list[0:100])
    shuffle(list)
    write_list(f, list[0:100])
    shuffle(list)
    write_list(f, list[0:100])
    shuffle(list)
    write_list(f, list[0:100])
    shuffle(list)
    write_list(f, list[0:100])
    shuffle(list)
    write_list(f, list[0:100])
    shuffle(list)
    write_list(f, list[0:100])
    shuffle(list)
    write_list(f, list[0:100])
    shuffle(list)
    write_list(f, list[0:100])

    f.close()

    G = networkx.Graph()
    for i in range(1000):
        G.add_node(i)

    for i in range(500000):
        x = random.randint(0, 999)
        y = random.randint(0, 999)
        if (x != y and not G.has_edge(x, y) and not G.has_edge(y, x)):
            G.add_edge(x, y)


    networkx.write_gml(G, "../deliverable1/inputs/large/graph.gml")

def generate_large_output():
    f = open("../deliverable1/outputs/large.out", "w")

    list = [i for i in range(1000)]
    shuffle(list)
    print(list)

    write_list(f, list[0:100])
    write_list(f, list[100:200])
    write_list(f, list[200:300])
    write_list(f, list[300:400])
    write_list(f, list[400:500])
    write_list(f, list[500:600])
    write_list(f, list[600:700])
    write_list(f, list[700:800])
    write_list(f, list[800:900])
    write_list(f, list[900:1000])

    f.close()

def generate_medium_input():
    f = open("../deliverable1/inputs/medium/parameters.txt", "w")

    list = [i for i in range(500)]
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
        x = random.randint(0, 499)
        y = random.randint(0, 499)
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
        f.write(", ")
    f.write("]\n")

def generate_small_input():
    # f = open("../deliverable1/inputs/small/parameters.txt", "w")
    #
    # write_rowdy_group(f, 0, 5)
    # write_rowdy_group(f, 5, 10)
    # write_rowdy_group(f, 10, 15)
    # write_rowdy_group(f, 15, 20)
    # write_rowdy_group(f, 20, 25)
    #
    # f.close()

    G = networkx.Graph()
    for i in range(27):
        G.add_node(i)

    add_friend_group(G, [0, 1, 2, 5])
    add_friend_group(G, [3, 4, 5])
    add_friend_group(G, [6, 7, 8])
    add_friend_group(G, [9, 10, 11])
    add_friend_group(G, [12, 13, 14])
    add_friend_group(G, [15, 16, 17])
    add_friend_group(G, [18, 19, 20])
    add_friend_group(G, [21, 22, 23])
    add_friend_group(G, [24, 25, 26])

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
        f.write(", ")
    f.write("]\n")

generate_input()