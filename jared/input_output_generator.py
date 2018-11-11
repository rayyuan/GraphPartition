import networkx

def generate_input():
    generate_large_input()

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

    write_rowdy_group(f, 0, 50)
    write_rowdy_group(f, 50, 100)
    write_rowdy_group(f, 100, 150)
    write_rowdy_group(f, 150, 200)
    write_rowdy_group(f, 200, 250)

    f.close()

    G = networkx.Graph()
    for i in range(250):
        G.add_node(i)

    add_edges_within(G, 0, 50)
    add_edges_within(G, 50, 100)
    add_edges_within(G, 100, 150)
    add_edges_within(G, 150, 200)
    add_edges_within(G, 200, 250)

    G.add_edge(49, 50)
    G.add_edge(49, 60)
    G.add_edge(49, 70)
    G.add_edge(49, 80)

    G.add_edge(149, 150)
    G.add_edge(149, 160)
    G.add_edge(149, 170)
    G.add_edge(149, 180)

    networkx.write_gml(G, "../deliverable1/inputs/medium/graph.gml")

def generate_small_input():
    f = open("../deliverable1/inputs/small/parameters.txt", "w")

    write_rowdy_group(f, 0, 5)
    write_rowdy_group(f, 5, 10)
    write_rowdy_group(f, 10, 15)
    write_rowdy_group(f, 15, 20)
    write_rowdy_group(f, 20, 25)

    f.close()

    G = networkx.Graph()
    for i in range(25):
        G.add_node(i)

    add_edges_within(G, 0, 5)
    add_edges_within(G, 5, 10)
    add_edges_within(G, 10, 15)
    add_edges_within(G, 15, 20)
    add_edges_within(G, 20, 25)

    G.add_edge(4, 5)
    G.add_edge(4, 6)
    G.add_edge(4, 7)
    G.add_edge(4, 8)

    G.add_edge(14, 15)
    G.add_edge(14, 16)
    G.add_edge(14, 17)
    G.add_edge(14, 18)

    networkx.write_gml(G, "../deliverable1/inputs/small/graph.gml")



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