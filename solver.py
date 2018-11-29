import networkx as nx
import os
from random import shuffle
import math
import numpy as np
import random


###########################################
# Change this variable to the path to 
# the folder containing all three input
# size category folders
###########################################
path_to_inputs = "./deliverable1/inputs"

###########################################
# Change this variable if you want
# your outputs to be put in a 
# different folder
###########################################
path_to_outputs = "./outputs"

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
    random_solution, num_people = find_random(graph, num_buses, size_bus)
    bus_list = np.zeros((num_buses, num_people))
    for i in range(len(random_solution)):
        for person in random_solution[i]:
            bus_list.itemset((i, int(person)), 1)

    r = nx.to_numpy_matrix(graph.to_undirected(), nodelist=graph.nodes)

    print(anneal(bus_list, r, num_buses, size_bus, num_people))

    return

def cost(s, r):
    bus_costs = s * r * s.T
    total_bus_cost = np.trace(bus_costs)
    return total_bus_cost

def take_step(starting_bus_seats,bus_count,size_bus,num_people):
    bus_seats = np.matrix(starting_bus_seats, copy=True)
    # bus_from, bus_to = np.random.choice(bus_count, 2, replace=False)
    #
    # bus_from_people = np.where(bus_seats[bus_from] == 1)
    # bus_to_people = np.where(bus_seats[bus_to] == 1)
    # people_in_bus_from = len(bus_from_people)
    # people_in_bus_to = len(bus_to_people)
    # bus_from_capacity = people_in_bus_from >= size_bus
    # bus_to_capacity = people_in_bus_to >= size_bus
    #
    # if bus_from_capacity and not bus_to_capacity:
    #     pos1 = np.random.choice(bus_from_people)
    #     pos2 = random.randint(num_people)
    # elif bus_to_capacity and not bus_from_capacity:
    #     pos1 = random.randint(num_people)
    #     pos2 = np.random.choice(bus_to_people)
    # elif bus_to_capacity and bus_from_capacity:
    #     pos1 = np.random.choice(bus_from_people)
    #     pos2 = np.random.choice(bus_to_people)
    # else:
    #     pos1 = random.randint(num_people)
    #     pos2 = random.randint(num_people)
    #
    # pos1_val = bus_seats[bus_from, pos1]
    # pos2_val = bus_seats[bus_to, pos2]
    # pos3_val = bus_seats[bus_to, pos1]
    # pos4_val = bus_seats[bus_from, pos2]
    # if(pos1_val ==1):
    #     bus_seats[bus_to, pos1] =1
    #     bus_seats[bus_from, pos1] = 0
    # if (pos1_val == 1):
    #     bus_seats[bus_to, pos1] = 1
    #     bus_seats[bus_from, pos1] = 0
    #
    # bus_seats[bus_from, pos2] =
    # bus_seats[bus_from, pos1] =
    # bus_seats[bus_to, pos1] =
    # bus_seats[bus_to, pos2] =
    bus_seats = np.matrix(starting_bus_seats, copy=True)
    person = random.randint(num_people)
    person_bus = 0
    for i in range(bus_count):
        if bus_seats[i][person] == 1:
            person_bus = i
            break
    if bus_count == 1:
        return bus_seats
    switch_bus = person_bus
    while switch_bus == person_bus:
        switch_bus = random.randint(bus_count)
    bus_seats[bus, person] = 0
    bus_seats[switch_bus, person] = 1
    people_in_switch = np.where(bus_seats[switch_bus] == 1)
    if len(people_in_switch) > size_bus:
        rand_person = np.random.choice(people_in_switch)
        bus_seats[bus, rand_person] = 1
        bus_seats[switch_bus, rand_person] = 0
    return bus_seats

def prob_accept(cost_old, cost_new, temp):
    a = 1 if cost_new < cost_old else np.exp((cost_old - cost_new) / temp)
    return a

def find_random(graph, num_buses, size_bus):
    nodes = graph.nodes()
    node_list = []
    for n in nodes:
        node_list.append(n)
    shuffle(node_list)
    rand_sol = []
    num_nodes = len(node_list)
    for i in range(num_buses):
        start = i * size_bus
        end = (i+1) * size_bus
        if end >= num_nodes:
            break
        rand_sol.append(node_list[start:end])
    return rand_sol, num_nodes


def anneal(pos_current, r, num_buses, size_bus, num_people, temp=1.0, temp_min=0.00001, alpha=0.9, n_iter=100, audit=False):
    cost_old = cost(pos_current, r)

    audit_trail = []

    while temp > temp_min:
        for i in range(0, n_iter):
            pos_new = take_step(pos_current, num_buses, size_bus, num_people)
            cost_new = cost(pos_new, r)
            p_accept = prob_accept(cost_old, cost_new, temp)
            if p_accept > np.random.random():
                pos_current = pos_new
                cost_old = cost_new
            if audit:
                audit_trail.append((cost_new, cost_old, temp, p_accept))
        temp *= alpha

    return pos_current, cost_old, audit_trail

def main():
    '''
        Main method which iterates over all inputs and calls `solve` on each.
        The student should modify `solve` to return their solution and modify
        the portion which writes it to a file to make sure their output is
        formatted correctly.
    '''
    size_categories = ["large", "medium", "large"]
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

            #TODO: modify this to write your solution to your 
            #      file properly as it might not be correct to 
            #      just write the variable solution to a file
            output_file.write(solution)

            output_file.close()

if __name__ == '__main__':
    main()


