The code for this project is written in Python (version 2.7).

The simulations take a lot of time to run. Please be patient.

=== Required external libraries ===
1. scipy
2. matplotlib


=== Conventions used ===
The immunization policies are enumerated as follows:
A - 1
B - 2
C - 3
D - 4

=== Code === 
The code is in the directory named Code. 
Solution to problem 1 is in the python file named problem_1.py
Solution to problem 2 is in the python file named problem_2.py
Solution to problem 3 is in 2 python files, namely, problem_3.py and problem_3_effective_strength.py

problem_3.py contains the simulation code for section 3.f
problem_3_effective_strength.py contains the simulation code for 3.e

To run the python scripts, it expects command line arguments to be passed. Please note the format below

For problem_1.py: python problem_1.py path_to_input_file
	eg. python problem_1.py /home/user/project/static.network

For problem_2.py: python problem_2.py path_to_input_file beta_value delta_value time_frames_per_simulation number_of_simulation_rounds
	eg. python problem_2.py /home/user/project/static.network 0.2 0.7 100 10

For problem_3.py: python problem_3.py path_to_input_file beta_value delta_value time_frames_per_simulation number_of_simulation_rounds no_of_vaccines immunization_policy_id
	eg. python problem_2.py /home/user/project/static.network 0.2 0.7 100 10 200 1
	NOTE: refer the conventions above for policy ID

For problem_3_effective_strength.py: python problem_3_effective_strength.py path_to_input_file immunization_policy_id vaccine_count_lower_limit vaccine_count_upper_limit vaccine_count_step
	eg. python problem_3_effective_strength.py /home/user/project/static.network 2 100 500 25
	NOTE: the vaccine count limits above are for running policy with variable vaccine counts. This is required since harding coding the limits to each policy is not a good idea


=== Images ===
The plot images are in the directory named Images

=== Simulation logs ===
The logs for the simulation are in the directory named Simulation logs.
These are only for the section 3.e

=== Report ===
The report for this project is in the pdf file named rgopalk_project_5.pdf

