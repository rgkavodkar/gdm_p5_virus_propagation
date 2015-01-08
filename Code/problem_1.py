__author__ = 'rg_kavodkar'
import sys
from scipy import linalg
import matplotlib.pyplot as pl

command_line_arguments = sys.argv
# Read the path from the command line arguments
dataset_filename_path = command_line_arguments[1]

# Given parameters
beta_1 = 0.2
beta_2 = 0.01
delta_1 = 0.7
delta_2 = 0.6

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

# Calculate the highest eigen value using the scipy.linalg.eigh API
highest_eigen_value = linalg.eigh(adjacency_matrix, eigvals_only=True, eigvals=(no_of_vertices-1, no_of_vertices-1))
# highest_eigen_value = 43.85469576
print "Highest Eigen Value: ", highest_eigen_value
print ""

# Calculate the effect virus strength for the given parametera
effective_virus_str = highest_eigen_value * beta_1 / delta_1
print "With parameter values beta =", beta_1, "and delta =", delta_1
print "Effective Virus Strength:", effective_virus_str
print ""

# An array of uniformly distributed probability values
prob_values = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

# The value of beta for threshold = 1, can be calculated as delta/highest_eigen_value
threshold_beta = delta_1/highest_eigen_value
print "Case 1: Beta value for Threshold = 1 is", threshold_beta

# Define some values below the beta threshold
below_threshold_values = []
for i in range(1, 6, 1):
    below_threshold_values.append(threshold_beta/5*i)

# Get the set of varying values
beta_values = below_threshold_values + prob_values

# Calculate the Effective Virus Strengths for each of the above values
varying_beta_evs = []
for i in beta_values:
    varying_beta_evs.append(highest_eigen_value * i / delta_1)

# The value of delta for threshold = 1, can be calculated as beta*highest_eigen_value
threshold_delta = beta_1 * highest_eigen_value
print "Case 1: Delta value for Threshold = 1 is", threshold_delta
print ""

# Get the set of varying values
delta_values = prob_values + [1]

# Calculate the Effective Virus Strengths for each of the above values
varying_delta_evs = []
for i in delta_values:
    varying_delta_evs.append(highest_eigen_value * beta_1 / i)

pl.plot(beta_values, varying_beta_evs)
pl.xlabel("Varying Beta values with Delta = 0.7")
pl.ylabel("Effective Virus strength")
pl.axhline(y=1, linewidth=2, color="r")
pl.show()

pl.plot(delta_values, varying_delta_evs)
pl.xlabel("Varying Delta values with Beta = 0.2")
pl.ylabel("Effective Virus strength")
pl.axhline(y=1, linewidth=2, color="r")
pl.show()


# Carry out the same calculations above for beta_2 and delta_2
effective_virus_str = highest_eigen_value * beta_2 / delta_2
print "With parameter values beta =", beta_2, "and delta =", delta_2
print "Effective Virus Strength:", effective_virus_str
print ""

# An array of uniformly distributed probability values
prob_values = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

# The value of beta for threshold = 1, can be calculated as delta/highest_eigen_value
threshold_beta = delta_2/highest_eigen_value

# Define some values below the beta threshold
below_threshold_values = []
for i in range(1, 6, 1):
    below_threshold_values.append(threshold_beta/5*i)

# Get the set of varying values
beta_values = below_threshold_values + prob_values
print "Case 2: Beta value for Threshold = 1 is", threshold_beta

# Calculate the Effective Virus Strengths for each of the above values
varying_beta_evs = []
for i in beta_values:
    varying_beta_evs.append(highest_eigen_value * i / delta_2)

# The value of delta for threshold = 1, can be calculated as beta*highest_eigen_value
threshold_delta = beta_2 * highest_eigen_value
print "Case 2: Delta value for Threshold = 1 is", threshold_delta

# Get the set of varying values
delta_values = prob_values + [1]

# Calculate the Effective Virus Strengths for each of the above values
varying_delta_evs = []
for i in delta_values:
    varying_delta_evs.append(highest_eigen_value * beta_2 / i)

pl.plot(beta_values, varying_beta_evs)
pl.xlabel("Varying Beta values with Delta = 0.6")
pl.ylabel("Effective Virus strength")
pl.axhline(y=1, linewidth=2, color="r")
pl.show()

pl.plot(delta_values, varying_delta_evs)
pl.xlabel("Varying Delta values with Beta = 0.01")
pl.ylabel("Effective Virus strength")
pl.axhline(y=1, linewidth=2, color="r")
pl.show()