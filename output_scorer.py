import os
import sys
import networkx as nx
import matplotlib.pyplot as plt

####################################################
# To run:
#   python3 output_scorer.py <input_folder> <output_file>
#
#   input_folder - the path to the input folder
#   output_file - the path to the output file
#
# Examples:
#   python3 output_scorer.py ./inputs/small/12 ./outputs/small/12.out
####################################################

def score_output(input_folder, output_file):
    '''
        Takes an input and an output and returns the score of the output on that input if valid
        
        Inputs:
            input_folder - a string representing the path to the input folder
            output_file - a string representing the path to the output file

        Outputs:
            (score, msg)
            score - a number between 0 and 1 which represents what fraction of friendships were broken
            msg - a string which stores error messages in case the output file is not valid for the given input
    '''
    graph = nx.read_gml(input_folder + "/graph.gml")
    parameters = open(input_folder + "/parameters.txt")
    num_buses = int(parameters.readline())
    size_bus = int(parameters.readline())
    constraints = []

    for line in parameters:
        line = line[1: -2]
        curr_constraint = [node.replace("'","") for node in line.split(", ")]
        constraints.append(curr_constraint)

    output = open(output_file)
    assignments = []
    for line in output:
        line = line[1: -2]
        curr_assignment = [node.replace("'","") for node in line.split(", ")]
        assignments.append(curr_assignment)

    if len(assignments) != num_buses:
        return -1, "Must assign students to exactly {} buses, found {} buses".format(num_buses, len(assignments))
    
    # make sure no bus is empty or above capacity
    for i in range(len(assignments)):
        if len(assignments[i]) > size_bus:
            return -1, "Bus {} is above capacity".format(i)
        if len(assignments[i]) <= 0:
            return -1, "Bus {} is empty".format(i)
        
    bus_assignments = {}
    attendance_count = 0
        
    # make sure each student is in exactly one bus
    attendance = {student:False for student in graph.nodes()}
    for i in range(len(assignments)):
        if not all([student in graph for student in assignments[i]]):
            return -1, "Bus {} references a non-existant student: {}".format(i, assignments[i])

        for student in assignments[i]:
            # if a student appears more than once
            if attendance[student] == True:
                print(assignments[i])
                return -1, "{0} appears more than once in the bus assignments".format(student)
                
            attendance[student] = True
            bus_assignments[student] = i
    
    # make sure each student is accounted for
    if not all(attendance.values()):
        return -1, "Not all students have been assigned a bus"
    
    total_edges = graph.number_of_edges()
    # Remove nodes for rowdy groups which were not broken up
    for i in range(len(constraints)):
        busses = set()
        for student in constraints[i]:
            busses.add(bus_assignments[student])
        if len(busses) <= 1:
            for student in constraints[i]:
                if student in graph:
                    graph.remove_node(student)

    # score output
    score = 0
    for edge in graph.edges():
        if bus_assignments[edge[0]] == bus_assignments[edge[1]]:
            score += 1
    score = score / total_edges


    return score, "Valid output submitted with score: {}".format(score)

def score_all():
    size_categories = ["small", "medium", "large"]

    log_file = open("outputs/score.log", "w")

    for size in size_categories:

        for input_folder in os.listdir(size):
            score, msg = score_output(size + "/" + input_folder, "outputs/" + size + "/" + input_folder + ".out")
            print(score, msg)
            log_file = open("outputs/score.log", "a")
            log_file.write(size + "/" + input_folder + "\t\t ------ \t\t" + str(score) + "\n")
            log_file.close()
            # input_name = os.fsdecode(input_folder)
            # if int(input_name) % int(sys.argv[1]) == int(sys.argv[2]):
            #     print("Thread: ", sys.argv[2], "--", size, input_name)
            #     log_file = open("outputs/runtime.log", "a")
            #     log_file.write("Thread: ")
            #     log_file.write(sys.argv[2])
            #     log_file.write(" -- ")
            #     log_file.write(size)
            #     log_file.write(" ")
            #     log_file.write(input_name)
            #     log_file.write("\n")
            #     log_file.close()
            #     graph, num_buses, size_bus, constraints = parse_input(category_path + "/" + input_name)
            #     solution = solve(graph, num_buses, size_bus, constraints)
            #     output_file = open(output_category_path + "/" + input_name + ".out", "w")
            #     buses = solution[0]
            #     count = 0
            #     for i in range(len(buses)):
            #         people = len(np.where(buses[i] == 1)[0])
            #         count += people
            #         #print("Bus " + str(i) + " has " + str(people) + " people.")
            #     # print("Total Num People After: " + str(count))
            #     labels = convert_to_labels(buses)
            #
            #     for i in range(len(labels)):
            #         bus = labels[i]
            #         write_list(output_file, bus)
            #     output_file.close()

if __name__ == '__main__':
    # score, msg = score_output(sys.argv[1], sys.argv[2])
    # print(msg)
    score_all()