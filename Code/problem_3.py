__author__ = 'rg_kavodkar'

import sys
import random
import math
import matplotlib.pyplot as pl
from copy import deepcopy
from scipy import linalg


command_line_arguments = sys.argv
# The path to the static.network file
dataset_filename_path = command_line_arguments[1]
# The value of beta, infection probability
beta = float(command_line_arguments[2])
# The value of delta, the healing probability
delta = float(command_line_arguments[3])
# Number of time splits in a simulation
times = int(command_line_arguments[4])
# Number of simulations
simulation_count = int(command_line_arguments[5])
# The number of vaccines
no_of_vaccines = int(command_line_arguments[6])
# The immunization policy to use
immunization_policy = int(command_line_arguments[7])

# dataset_filename_path = "/home/rg_kavodkar/Downloads/static.network"
#
# simulation_count = 10
#
# times = 100
#
# beta_1 = 0.2
# beta_2 = 0.01
# delta_1 = 0.7
# delta_2 = 0.6
#
# no_of_vaccines = 200
#
# immunization_policy = 1


# function to get the neighbors of a given node
def get_neighbors(adjacency_matrix, node, no_of_vertices):
    neighbors = []
    for j in range(0,no_of_vertices):
        if adjacency_matrix[node][j] == 1:
            neighbors.append(j)
    return neighbors


# Removes said edges from the corresponding adjacency Matrix
def removes_edges(adjacency_matrix, nodes):
    for i in nodes:
        for j in range(no_of_vertices):
            adjacency_matrix[i][j] = 0
            adjacency_matrix[j][i] = 0


# Immunization policies definition
# The policy code is enumerated as follows
# 1 == A
# 2 == B
# 3 == C
# 4 == D
def immunize(adjacency_matrix, no_of_vertices, policy):
    nodes_for_vaccines = []

    if policy == 1:
        # Policy A: select no_of_vaccines nodes randomly

        # Get K random nodes for vaccines
        nodes_for_vaccines = random.sample(range(0, no_of_vertices), no_of_vaccines)

        # Remove the edges of the nodes in the nodes_for_vaccines list
        removes_edges(adjacency_matrix, nodes_for_vaccines)

    elif policy == 2:
        # Policy B: select no_of_vaccines nodes with highest degrees

        # List to hold the node degrees, intialized to 0s
        node_degrees = [0]*no_of_vertices
        # Calculate the degree of each node
        for i in range(no_of_vertices):
            node_degrees[i] = adjacency_matrix[i].count(1)

        # Counter for no_of_vaccines
        count = no_of_vaccines

        # In this loop, get K nodes with highest degrees
        while count > 0:
            count -= 1
            # Get the highest degree node in the current iteration
            highest_degree_node = node_degrees.index(max(node_degrees))

            # Append the highest degree node to the vaccination list
            nodes_for_vaccines.append(highest_degree_node)

            # Set that node's degree to -1 since it is already considered
            # and shouldn't interfere in the successive iterations
            node_degrees[highest_degree_node] = -1

        # Remove the edges of the nodes in the nodes_for_vaccines list
        removes_edges(adjacency_matrix, nodes_for_vaccines)

    elif policy == 3:
        # Policy C: Select the node with the highest degree for immunization.
        # Remove this node (and its incident edges) from the contact network.
        # Repeat until all vaccines are administered

        # List to hold the node degrees, intialized to 0s
        node_degrees = [0]*no_of_vertices

        # Counter for no_of_vaccines
        count = no_of_vaccines
        # In this loop, get K nodes with highest degrees
        while count > 0:
            count -= 1

            # Calculate the degree of each node in each iteration
            for i in range(no_of_vertices):
                node_degrees[i] = adjacency_matrix[i].count(1)

            # Get the highest degree node in the current iteration
            highest_degree_node = node_degrees.index(max(node_degrees))

            # Append the highest degree node to the vaccination list
            nodes_for_vaccines.append(highest_degree_node)

            # Remove the edges of the corresponding node
            removes_edges(adjacency_matrix, [highest_degree_node])

        # Restore the adjacency matrix to its original content from reserve_adjacency
        adjacency_matrix = deepcopy(reserve_adjacency)

        # Remove the edges of the nodes in the nodes_for_vaccines list
        removes_edges(adjacency_matrix, nodes_for_vaccines)

    elif policy == 4:
        # Policy D: Find the eigenvector corresponding to the largest eigenvalue
        # of the contact networks adjacency matrix. Find the k largest (absolute)
        # values in the eigenvector. Select the k nodes at the corresponding
        # positions in the eigenvector

        # Get the highest_eigen_value and its corresponding eigen vector
        highest_eigen_value, eigen_vector = linalg.eigh(adjacency_matrix, eigvals=(no_of_vertices-1, no_of_vertices-1))
        absolute_eigen_vector = []

        # Convert the values in the eigen vector to their absolute values
        for i in range(len(eigen_vector)):
            eigen_vector[i] = math.fabs(eigen_vector[i][0])

        for i in range(len(eigen_vector)):
            absolute_eigen_vector.append(eigen_vector[i][0])

        # Counter for no_of_vaccines
        count = no_of_vaccines

        # Get the indices of the K largest values in the eigen vectors
        # These indices correspond to the indices of the nodes to immunize
        while count > 0:
            count -= 1
            # Get the highest degree node in the current iteration
            highest_degree_node = absolute_eigen_vector.index(max(absolute_eigen_vector))

            # Append the highest degree node to the vaccination list
            nodes_for_vaccines.append(highest_degree_node)

            # Set that node's degree to -1 since it is already considered
            # and shouldn't interfere in the successive iterations
            absolute_eigen_vector[highest_degree_node] = 0

        # Remove the edges of the nodes in the nodes_for_vaccines list
        removes_edges(adjacency_matrix, nodes_for_vaccines)


# Read all the lines from the given dataset
data_set = open(dataset_filename_path, 'r').readlines()

# Get the number of vertices in the network, ie, the first number in the first line
no_of_vertices = int(data_set[0].strip().split(" ")[0])

# Get the number of edges in the network, ie, the second number in the first line
no_of_edges = int(data_set[0].strip().split(" ")[1])

# No of infected nodes
no_of_infected = no_of_vertices / 10

# Initialize an array of size no_of_vertices*no_of_vertices
adjacency_matrix = []
for rows in range(no_of_vertices):
    adjacency_matrix.append([0]*no_of_vertices)

# Read all the edges in the network and add corresponding entries into the adjacency matrix
# Adding + 1 since range excludes the upper limit
for i in range(1, no_of_edges + 1):
    vertex_1 = int(data_set[i].strip().split(" ")[0])
    vertex_2 = int(data_set[i].strip().split(" ")[1])
    # adding 2 entries into the adjacency matrix since it is symmetrical and undirected
    adjacency_matrix[vertex_1][vertex_2] = 1
    adjacency_matrix[vertex_2][vertex_1] = 1

# Keep a reserve copy of the adjacency_matrix since we play around with the edges with multiple policies
reserve_adjacency = deepcopy(adjacency_matrix)

# Dictionary to hold the dictionary of infected_fraction over the simulations
simulation_wise_infected_fraction = {}

# Do the simulation simulation_count times
for sim in range(0, simulation_count):
    print "Running Simulation round", (sim + 1)
    # Randomly select n/10 samples as infected
    infected_nodes = random.sample(range(0, no_of_vertices), no_of_infected)

    # perform the immunization
    immunize(adjacency_matrix, no_of_vertices, immunization_policy)

    # Dictionary that holds the fraction of infected
    infected_fraction = {}

    for i in range(0, times):
        # Define a set to hold the newly infected nodes in this iteration
        new_infected_nodes = set()
        # An array to hold the healed nodes in this iteration
        healed_nodes = []

        susceptible_neighbors = []
        # Spread the infection
        for infected in infected_nodes:
            # Get the susceptible neighbors of the infected node
            susceptible_neighbors.extend(get_neighbors(adjacency_matrix, infected, no_of_vertices))
            # For each of the susceptible node, generate a random number to decide if it will get infected

        # susceptible_neighbors = set(susceptible_neighbors)
        for susceptible in susceptible_neighbors:
            # If the neighbor is already infected_nodes list, skip
            if susceptible in infected_nodes:
                continue
            # Generate a random number
            random_infection_probability = random.random()
            # If the generated random number is greater than the beta value, add it to the new_infected list
            if random_infection_probability <= beta:
                new_infected_nodes.add(susceptible)

        # Check for healing
        for infected in infected_nodes:
            # Generate a random number to decide the healing
            random_healing_probability = random.random()
            # If the generated random number is greater than the delta value, remove it from the infected_list
            if random_healing_probability <= delta:
                healed_nodes.append(infected)

        # Remove the healed nodes from the infected list
        for healed in healed_nodes:
            infected_nodes.remove(healed)

        # Add the new_infected list to the infected list
        for new_infected in new_infected_nodes:
            infected_nodes.append(new_infected)

        # Calculate the fraction of nodes that is infected at time = i
        fraction = len(infected_nodes)/float(no_of_vertices)

        # Add the fraction to the dictionary
        infected_fraction[i] = fraction

    # Add this simulations timewise infected fraction to a dictionary
    simulation_wise_infected_fraction[sim] = infected_fraction
    # Restore the actual adjacency matrix
    adjacency_matrix = deepcopy(reserve_adjacency)

# Array to hold the average fraction values
average_infected_fraction = [0]*times

# Array to hold the overall sum of each time
sum_infection_timed = [0]*times

# Loop through the simulation_wise_infected_fraction dictionary to calculate the aum and average
for i in range(simulation_count):
    fraction = simulation_wise_infected_fraction[i]
    for j in range(times):
        sum_infection_timed[j] += fraction[j]

for i in range(times):
    average_infected_fraction[i] = sum_infection_timed[i] / simulation_count

pl.plot(range(times), average_infected_fraction)
plot_title = "Plot of time vs avg infected fraction for Policy " + str(immunization_policy)
pl.title(plot_title)
pl.xlabel("Time")
pl.ylabel("Average infected fraction")
pl.show()


print "Done.."