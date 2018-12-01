import networkx as nx
import os
import numpy as np
import random
import sys

np.set_printoptions(threshold=np.nan)

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

def main():
    '''
        Main method which iterates over all inputs and calls `solve` on each.
        The student should modify `solve` to return their solution and modify
        the portion which writes it to a file to make sure their output is
        formatted correctly.
    '''
    if sys.argv[1] == "--file":
        graph, num_buses, size_bus, constraints = parse_input(sys.argv[2])
        solution = solve(graph, num_buses, size_bus, constraints)
        labels = convert_to_labels(solution[0])
        output_file = open("outputs/" + sys.argv[2] + ".out", "w")

        for i in range(len(labels)):
            bus = labels[i]
            write_list(output_file, bus)
        output_file.close()
    else:
        # log_file = open("outputs/runtime.log", "w")
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
                if int(input_name) % int(sys.argv[1]) == int(sys.argv[2]):
                    print("Thread: ", sys.argv[2], "--", size, input_name)
                    log_file = open("outputs/runtime.log", "a")
                    log_file.write("Thread: ")
                    log_file.write(sys.argv[2])
                    log_file.write(" -- ")
                    log_file.write(size)
                    log_file.write(" ")
                    log_file.write(input_name)
                    log_file.write("\n")
                    log_file.close()

                    graph, num_buses, size_bus, constraints = parse_input(category_path + "/" + input_name)
                    solution = solve(graph, num_buses, size_bus, constraints)
                    labels = convert_to_labels(solution[0])
                    output_file = open(output_category_path + "/" + input_name + ".out", "w")

                    for i in range(len(labels)):
                        bus = labels[i]
                        write_list(output_file, bus)
                    output_file.close()


def write_list(f, list):
    if len(list) is 0:
        return
    f.write("[")
    for i in range(len(list)):
        f.write("'")
        f.write(str(list[i]))
        f.write("'")
        if i is not len(list) - 1:
            f.write(", ")
    f.write("]\n")


def solve(graph, num_buses, size_bus, constraints):
    # TODO: Write this method as you like. We'd recommend changing the arguments here as well

    # generate list of nodes
    node_list = []
    for n in graph.nodes:
        node_list.append(n)

    # generate label / id mapping
    for i in range(len(node_list)):
        label_to_id[node_list[i]] = i
        id_to_label[i] = node_list[i]

    # generate starting solution
    s = gen_starting_solution(num_buses, node_list, graph, constraints)

    # generate relationship matrix
    r = (nx.to_numpy_matrix(graph.to_undirected(), nodelist=graph.nodes) * -1).A

    return anneal(s, r, size_bus, constraints)

def gen_starting_solution(num_buses, node_list, graph, constraints):
    s = np.zeros((num_buses, len(node_list)))

    #generate random
    for i in range(len(node_list)):
        s.itemset((random.randint(0, num_buses - 1), i), 1)

    return s

def anneal(s, r, size_bus, constraints, temp=1.0, temp_min=0.00001, alpha=0.9, n_iter=50):
    cost_old = cost(s, r, constraints)

    while temp > temp_min:
        for i in range(0, n_iter):
            # print(s.sum(axis=1), i, cost_old)
            s_new = take_step(s, size_bus) # here
            cost_new = cost(s_new, r, constraints)
            p_accept = prob_accept(cost_old, cost_new, temp)
            if p_accept > np.random.random():
                s = s_new
                cost_old = cost_new
        # print("cost: ", cost_old)
        temp *= alpha

    return s, cost_old

def convert_to_labels(buses):
    labels = []
    count = 0
    for i in range(len(buses)):
        bus = buses[i]
        bus_labels = []
        for x in range(len(bus)):
            if bus[x] == 1:
                bus_labels.append(id_to_label[x])
        labels.append(bus_labels)
        count += len(bus_labels)
    #print(labels)
    # print("added: ", count, "people.")
    return labels

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

def prob_accept(cost_old, cost_new, temp):
    if cost_new < cost_old:
        a = 1
        #print(cost_new, temp)
    else:
        a = np.exp((cost_old - cost_new) / temp)
    return a

def take_step(s, size_bus):
    s_copy = np.array(s, copy=True)

    if(s_copy.shape[0] == 1):
        return s_copy

    person_to_swap = random.randint(0, s_copy.shape[1] - 1)
    for i in range(s_copy.shape[0]):
        if s_copy[i, person_to_swap] == 1:
            from_row = i
            s_copy.itemset((i, person_to_swap), 0)
    to_row = random.randint(0, s_copy.shape[0] - 1)
    s_copy.itemset((to_row, person_to_swap), 1)

    if np.sum(s_copy[to_row, :]) > size_bus or random.randint(0, 2) == 0 or np.sum(s_copy[from_row, :]) == 0:
        other_person_to_swap = np.where(s_copy[to_row, :] == 1)[0]
        other_person_to_swap = other_person_to_swap[random.randint(0, len(other_person_to_swap) - 1)]
        s_copy[to_row, other_person_to_swap] = 0
        s_copy[from_row, other_person_to_swap] = 1

    return s_copy




if __name__ == '__main__':
    main()



