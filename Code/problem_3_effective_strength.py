__author__ = 'rg_kavodkar'
import sys
import random
from copy import deepcopy
from scipy import linalg
import matplotlib.pyplot as pl
import math

command_line_arguments = sys.argv
# The path to the static.network file
dataset_filename_path = command_line_arguments[1]

# The immunization policy to use
immunization_policy = int(command_line_arguments[2])

# The limits of the vaccine count
vaccine_count_lower_limit = int(command_line_arguments[3])
vaccine_count_upper_limit = int(command_line_arguments[4])
vaccine_count_step = int(command_line_arguments[5])

print "Immunization Policy", immunization_policy
print "Given Lower limit", vaccine_count_lower_limit
print "Given Upper Limit", vaccine_count_upper_limit
print "Given Step", vaccine_count_step

# given parameter values for beta and delta
beta = 0.2
delta = 0.7


# function to convert number to log base 10
def convert_to_log(num):
    return math.log(num)


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

varying_vaccine_count = []
varying_evs_values = []

for k in range(vaccine_count_lower_limit, vaccine_count_upper_limit, vaccine_count_step):
    # Assign value to no_of_vaccines
    no_of_vaccines = k
    print "No. of vaccines:", no_of_vaccines

    # Perform immunization
    immunize(adjacency_matrix, no_of_vertices, immunization_policy)

    # Calculate the highest eigen value using the scipy.linalg.eigh API
    highest_eigen_value = linalg.eigh(adjacency_matrix, eigvals_only = True, eigvals = (no_of_vertices-1, no_of_vertices-1))

    print "Highest Eigen Value: ", highest_eigen_value

    # Calculate the effect virus strength for the given parametera
    effective_virus_str = highest_eigen_value * beta / delta
    print "With parameter values beta =", beta, "delta =", delta
    print "Effective Virus Strength:", effective_virus_str
    print ""
    varying_vaccine_count.append(k)
    varying_evs_values.append(effective_virus_str)
    adjacency_matrix = deepcopy(reserve_adjacency)
print "****************"

pl.plot(varying_vaccine_count, varying_evs_values)
pl.xlabel("Varying vaccines count")
pl.ylabel("Effective Virus strength")
pl.axhline(y=1, linewidth=2, color="r")
pl.show()
