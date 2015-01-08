__author__ = 'rg_kavodkar'

import sys
import random
import matplotlib.pyplot as pl

command_line_arguments = sys.argv
# dataset_filename_path = command_line_arguments[1]
dataset_filename_path = command_line_arguments[1]
# Beta value
beta = float(command_line_arguments[2])
# Delta value
delta = float(command_line_arguments[3])
# Number of time frames in a simulation
times = int(command_line_arguments[4])
# Number of simulations
simulation_count = int(command_line_arguments[5])

#
# dataset_filename_path = "/home/rg_kavodkar/Downloads/static.network"
#
# # No of simulations
# simulation_count = 10
#
# # No of time frames
# times = 100
#
# # Given parameters
# beta_1 = 0.2
# beta_2 = 0.01
# delta_1 = 0.7
# delta_2 = 0.6


# function to get the neighbors of a given node
def get_neighbors(adjacency_matrix, node, no_of_vertices):
    neighbors = []
    for j in range(0,no_of_vertices):
        if adjacency_matrix[node][j] == 1:
            neighbors.append(j)
    return neighbors


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

# Dictionary to hold the dictionary of infected_fraction over the simulations
simulation_wise_infected_fraction = {}

# Do the simulation simulation_count times
for sim in range(0, simulation_count):
    print "Running Simulation round", (sim + 1)
    # Randomly select n/10 samples as infected
    infected_nodes = random.sample(range(0, no_of_vertices), no_of_infected)

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

print "Done gathering simulation info.."

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
pl.xlabel("Time")
pl.ylabel("Average Infected Fraction")
pl.show()


print "Done.."