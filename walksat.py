import matplotlib.pyplot as plt
import csv
import sys
import math
import copy
import subprocess
import statistics
from random import *
from time import time


# TODO: Have some sort of data structure here that holds each WalkSAT result numbers
# e.g. number of clauses, number of "flips", did it terminate successfuly?

NUM_VARIABLES = 20

def run():
    init_problem_generator()
    generate_and_solve_problems()
    clean_up()

# Calls `make` on the terminal to produce the makewff binary executable
def init_problem_generator():
    subprocess.call(["make"])

# For N fixed at 20, generate 50 random 3SAT problems for each value
# of C/N from 1 to 10 (so, with C ranging from 20, 40, …, 200). The total
# number of generated 3SAT problems should therefore be 500.
def generate_and_solve_problems():
    num_clauses = 20
    while num_clauses < 200:
        set_flips = []
        set_successes = 0
        print(f'** About to run WalkSAT 50 times with N = {NUM_VARIABLES} and C = {num_clauses} **')
        for i in range(50):
            problem = generate_problem(num_clauses)
            num_flips, success = walksat(problem)
            if (success):
                set_flips.append(num_flips)
                set_successes += 1
        print(f'** Finished running WalkSAT 50 times with N = {NUM_VARIABLES} and C = {num_clauses} **')
        print(f'** Results: Median flips = {statistics.median(set_flips)}, Number of successes = {set_successes}\n\n')
        num_clauses += 20

# Calls makewff to generate a 3-SAT problem with 20 variables and the given
# number of clauses - encoded in an array of strings where each string is
# a clause (e.g. ['20 -19 3 0', '2 -15 -12'] has two clauses)
def generate_problem(num_clauses):
    problem = subprocess.check_output(["./makewff", "-cnf", "3",
                                        str(NUM_VARIABLES), str(num_clauses)])

    # Converts bytes to string then into a trimmed array of strings with
    # only the clauses
    return parse(problem.decode('utf-8').split("\n")[2:])

# Takes in a 3-SAT problem encoded as an array of strings (e.g. ['20 -19 3 0',
# '2 -15 -12'] has two clauses) and runs WalkSAT on it for 10 seconds at maximum
#
# Returns a pair (number, boolean) of the number of flips and True if the
# problem was solved, False otherwise
def walksat(problem):
    # 1. Generate random interpretation
    interpretation = generate_interpretation()
    end = time() + 10
    num_flips = 0
    while time() < end:
        # 2. Get unsatisfied clauses
        unsatisfied_clauses = get_unsatisfied_clauses(problem, interpretation)

        # 3. Check if problem is solved
        if(len(unsatisfied_clauses) == 0):
            return num_flips, True

        # 4.  Pick one unsatisfied clause at random
        random_unsatisfied_clause = unsatisfied_clauses[randint(0, len(unsatisfied_clauses) - 1)]

        # 5. Pick an atom to flip (randomly 5.1 or 5.2)
            # 5.1 Randomly
            # 5.2 To minimize # of unsatisfied clauses
        randomly_flip(interpretation, random_unsatisfied_clause) if(randint(1,2) == 1) else minimize_unsatisfied_clauses(interpretation, random_unsatisfied_clause, problem)
        num_flips += 1

    # Stop with failure after 10 seconds
    return num_flips, False

# Randomly pick an atom in the clause and flip it
def randomly_flip(interpretation, clause):
    randindex = randint(0, 2)
    interpretation[abs(clause[randindex])] *= -1

# Flips one atom in the_chosen_clause that minimizes the # of unsatisfied
# clauses in the problem
def minimize_unsatisfied_clauses(interpretation, the_chosen_clause, problem):
    var_to_flip = 0
    min_so_far = 21

    for var in the_chosen_clause:
        interpretation_copy = copy.deepcopy(interpretation)
        interpretation_copy[abs(var)] *= -1
        num_unsatisfied_clauses = len(get_unsatisfied_clauses(problem, interpretation_copy))
        if (num_unsatisfied_clauses < min_so_far):
            var_to_flip = var
            min_so_far = num_unsatisfied_clauses

    interpretation[abs(var_to_flip)] *= -1

# Generates a random interpretation with twenty variables
def generate_interpretation():
    interpretation = [0]
    for i in range(1, 21):
        random_ass = i * (-1) if randint(0,1) == 0 else i
        interpretation.append(random_ass)

    return interpretation

# Takes all clauses and the interpretation so far and returns all unsatisfied
def get_unsatisfied_clauses(problem, interpretation):
    unsatisfied_clauses = []
    for clause in problem:
        if(clause[0] != interpretation[abs(clause[0])] and
           clause[1] != interpretation[abs(clause[1])] and
           clause[2] != interpretation[abs(clause[2])]):
            unsatisfied_clauses.append(clause)

    return unsatisfied_clauses

# Takes generated 3-SAT problem and parses it into a list of list
# (e.g. ['20 -19 3 0', '2 -15 -12 0'] -> [[20, -19, 3],[2, -15, -12]])
def parse(problem):
    parsed_problem = []
    for clause in problem[:-1]:
        parsed_clause = []
        for var in clause.split(' ')[:-1]:
            parsed_clause.append(int(var))
        parsed_problem.append(parsed_clause)

    return parsed_problem

# Calls `make clean` on the terminal to clean up makewff binary executable
def clean_up():
    subprocess.call(["make", "clean"])

if __name__ == '__main__':
    run()
