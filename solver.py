import networkx as nx
import os
import numpy as np
import random
import sys


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
passenger_count = {}

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

def gen_starting_solution(num_buses, node_list, graph, constraints):
    s = np.zeros((num_buses, len(node_list)))

    #generate random
    for i in range(len(node_list)):
        s.itemset((random.randint(0, num_buses - 1), i), 1)

    return s

def solve(graph, num_buses, size_bus, constraints):
    random_solution, num_people, max_degree = find_random(graph, num_buses, size_bus)
    bus_list = np.zeros((num_buses, num_people))
    count = 0
    for i in range(len(random_solution)):
        for person in random_solution[i]:
            bus_list.itemset((i, int(person)), 1)
            count += 1

    # print("Started with: ", count, " people")

    node_list = []
    node_list_degrees = []
    # print(node_list_degrees)
    for (node, degree) in graph.degree():
        node_list.append(node)
        node_list_degrees.append(degree)

    r = nx.to_numpy_matrix(graph.to_undirected(), nodelist=graph.nodes) * -1
    r = r.A

    # for i in range(len(node_list)):
    #     for j in range(len(node_list)):
    #         if r[i, j] == -1:
    #             r.itemset((i, j), -(node_list_degrees[i] / max(node_list_degrees)))
    # print(type(r))
    # print(r)

    solution = anneal(bus_list, r, num_buses, size_bus, constraints)

    return solution


def cost(s, r, constraints):
    s_copy = np.array(s, copy=True)
    for i in range(len(s_copy)):
        if not check_row(s_copy[i], constraints):
            s_copy[i] = 0
    bus_costs = np.dot(np.dot(s_copy, r), s_copy.T)
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


def take_step(starting_bus_seats, bus_count, size_bus):
    bus_seats = np.array(starting_bus_seats, copy=True)
    if bus_count == 1:
        return bus_seats

    people = []
    person_bus = 0
    people_in_person_bus = 0
    while people_in_person_bus < 2:
        person_bus = random.randint(0, bus_count-1)
        people = np.where(bus_seats[person_bus] == 1)[0]
        people_in_person_bus = len(people)

    person = np.random.choice(people)


    switch_bus = person_bus
    while switch_bus == person_bus:
        switch_bus = random.randint(0, bus_count-1)

    bus_seats[person_bus, person] = 0
    bus_seats[switch_bus, person] = 1
    people_in_switch = np.where(bus_seats[switch_bus] == 1)[0]

    if len(people_in_switch) > size_bus:
        rand_person = np.random.choice(people_in_switch)
        bus_seats[person_bus, rand_person] = 1
        bus_seats[switch_bus, rand_person] = 0
    return bus_seats


def prob_accept(cost_old, cost_new, temp):
    if cost_new < cost_old:
        a = 1
        #print(cost_new, temp)
    else:
        a = np.exp((cost_old - cost_new) / temp)
    return a


def find_random(graph, num_buses, size_bus):
    node_list = []
    i = 0
    max_degree = 0
    for n in graph.nodes():
        deg_n = graph.degree(n)
        if deg_n > max_degree:
            max_degree = max_degree
        node_list.append(i)
        id_to_label[i] = n
        label_to_id[n] = i
        i += 1

    rand_sol = []
    num_nodes = len(node_list)
    for i in range(num_buses):
        rand_sol.append([])

    for i in range(num_nodes):
        rand_bus_index = random.randint(0, num_buses-1)
        rand_bus = rand_sol[rand_bus_index]
        while len(rand_bus) >= size_bus:
            rand_bus_index = random.randint(0, num_buses - 1)
            rand_bus = rand_sol[rand_bus_index]
        rand_bus.append(node_list[i])

    while len(rand_sol) < num_buses:
        rand_sol.append([])


    # for i in range(num_nodes):
    #     rand_bus_index = random.randint(0, num_buses-1)
    #     rand_bus = rand_sol[rand_bus_index]
    #     while len(rand_bus) >= size_bus:
    #         rand_bus_index = random.randint(0, num_buses - 1)
    #         rand_bus = rand_sol[rand_bus_index]
    #     rand_bus.append(node_list[i])

    empty_buses = []
    for i in range(num_buses):
        if len(rand_sol[i]) == 0:
            empty_buses.append(i)

    i = 0
    for x in range(len(empty_buses)):
        bus = rand_sol[empty_buses[x]]
        bus_to_take_from = rand_sol[i]
        while len(bus_to_take_from) < 2:
            i -= 1
            bus_to_take_from = rand_sol[i]
        bus.append(bus_to_take_from.pop(len(bus_to_take_from)-1))
        i += 1

    return rand_sol, num_nodes, max_degree


def anneal(pos_current, r, num_buses, size_bus, constraints, temp=1.0, temp_min=0.00001, alpha=0.93, n_iter=400):
    cost_old = cost(pos_current, r, constraints)
    while temp > temp_min:
        for i in range(0, n_iter):
            pos_new = take_step(pos_current, num_buses, size_bus)
            cost_new = cost(pos_new, r, constraints)
            p_accept = prob_accept(cost_old, cost_new, temp)
            if p_accept > np.random.random():
                pos_current = pos_new
                cost_old = cost_new
        # print(cost_new, temp, temp_min)
        temp *= alpha

    return pos_current, cost_old

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
            if int(input_name) % int(sys.argv[1]) == int(sys.argv[2]):
                print("Solving: ", size, input_name)
                graph, num_buses, size_bus, constraints = parse_input(category_path + "/" + input_name)
                solution = solve(graph, num_buses, size_bus, constraints)
                output_file = open(output_category_path + "/" + input_name + ".out", "w")
                buses = solution[0]
                count = 0
                for i in range(len(buses)):
                    people = len(np.where(buses[i] == 1)[0])
                    count += people
                    #print("Bus " + str(i) + " has " + str(people) + " people.")
                # print("Total Num People After: " + str(count))
                labels = convert_to_labels(buses)

                for i in range(len(labels)):
                    bus = labels[i]
                    write_list(output_file, bus)
                output_file.close()

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

if __name__ == '__main__':
    main()


