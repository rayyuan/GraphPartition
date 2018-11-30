import networkx as nx
import os
import numpy as np
import random

###########################################
# Change this variable to the path to
# the folder containing all three input
# size category folders
###########################################
path_to_inputs = "./"

###########################################
# Change this variable if you want
# your outputs to be put in a
# different folder
###########################################
path_to_outputs = "./outputs"

label_to_id = {}
id_to_label = {}

def parse_input(folder_name):
    '''
        Parses an input and returns the corresponding graph and parameters

        Inputs:
            folder_name - a string representing the path to the input folder

        Outputs:
            (graph, num_buses, size_bus, constraints)
            graph - the graph as a NetworkX object
            num_buses - an integer representing the number of buses you can allocate to
            size_buses - an integer representing the number of students that can fit on a bus
            constraints - a list where each element is a list vertices which represents a single rowdy group
    '''
    graph = nx.read_gml(folder_name + "/graph.gml")
    parameters = open(folder_name + "/parameters.txt")
    num_buses = int(parameters.readline())
    size_bus = int(parameters.readline())
    constraints = []

    for line in parameters:
        line = line[1: -2]
        curr_constraint = [num.replace("'", "") for num in line.split(", ")]
        constraints.append(curr_constraint)

    return graph, num_buses, size_bus, constraints


def solve(graph, num_buses, size_bus, constraints):
    # TODO: Write this method as you like. We'd recommend changing the arguments here as well

    node_list = []
    for n in graph.nodes:
        node_list.append(n)

    for i in range(len(node_list)):
        label_to_id[node_list[i]] = i
        id_to_label[i] = node_list[i]

    s = gen_starting_solution(num_buses, node_list, graph, constraints)
    r = nx.to_numpy_matrix(graph.to_undirected(), nodelist=graph.nodes) * -1

    print(s)
    print(r)

def gen_starting_solution(num_buses, node_list, graph, constraints):
    s = np.zeros((num_buses, len(node_list)))

    #generate random
    for i in range(len(node_list)):
        s.itemset((random.randint(0, num_buses - 1), i), 1)

    return s

def anneal(pos_current, r, num_buses, size_bus, constraints, temp=1.0, temp_min=0.00001, alpha=0.9, n_iter=100):
    cost_old = cost(pos_current, r, constraints)

    while temp > temp_min:
        for i in range(0, n_iter):
            pos_new = take_step(pos_current, num_buses, size_bus)
            cost_new = cost(pos_new, r, constraints)
            print(cost_new)
            p_accept = prob_accept(cost_old, cost_new, temp)
            if p_accept > np.random.random():
                pos_current = pos_new
                cost_old = cost_new
        temp *= alpha

    return pos_current, cost_old

def cost(s, r, constraints):
    s_copy = np.matrix(s, copy=True)
    for i in range(len(s_copy)):
        if not check_row(s_copy[i], constraints):
            s_copy[i] = 0
    bus_costs = s_copy * r * s_copy.T
    total_bus_cost = np.trace(bus_costs)
    return total_bus_cost


def check_row(row, constraints):
    permissible = True
    for list in constraints:
        people_in_curr_bus = set(np.where(row[0] == 1)[0])
        permissible = permissible and not people_in_curr_bus.issubset(list)
        if not permissible:
            return False
    return permissible


def main():
    '''
        Main method which iterates over all inputs and calls `solve` on each.
        The student should modify `solve` to return their solution and modify
        the portion which writes it to a file to make sure their output is
        formatted correctly.
    '''
    size_categories = ["small", "medium", "large"]
    if not os.path.isdir(path_to_outputs):
        os.mkdir(path_to_outputs)

    for size in size_categories:
        category_path = path_to_inputs + "/" + size
        output_category_path = path_to_outputs + "/" + size
        category_dir = os.fsencode(category_path)

        if not os.path.isdir(output_category_path):
            os.mkdir(output_category_path)

        for input_folder in os.listdir(category_dir):
            input_name = os.fsdecode(input_folder)
            graph, num_buses, size_bus, constraints = parse_input(category_path + "/" + input_name)
            solution = solve(graph, num_buses, size_bus, constraints)
            output_file = open(output_category_path + "/" + input_name + ".out", "w")

            # TODO: modify this to write your solution to your
            #      file properly as it might not be correct to
            #      just write the variable solution to a file
            output_file.write(solution)

            output_file.close()


if __name__ == '__main__':
    main()



