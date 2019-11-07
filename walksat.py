import matplotlib.pyplot as plt
import csv
import sys
import math
from random import *
import subprocess

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
        for i in range(50):
            problem = generate_problem(num_clauses)
            # TODO: Solve the generated problem with WalkSAT and save the
            # results
            walksat(problem)
        num_clauses += 20

# Calls makewff to generate a 3-SAT problem with 20 variables and the given
# number of clauses - encoded in an array of strings where each string is
# a clause (e.g. ['20 -19 3 0', '2 -15 -12'] has two clauses)
def generate_problem(num_clauses):
    problem = subprocess.check_output(["./makewff", "-cnf", "3",
                                        str(NUM_VARIABLES), str(num_clauses)])

    # Converts bytes to string then into a trimmed array of strings with
    # only the clauses
    return problem.decode('utf-8').split("\n")[2:]

# Takes in a 3-SAT problem encoded as an array of strings (e.g. ['20 -19 3 0',
# '2 -15 -12'] has two clauses) and solves it using WalkSAT
def walksat(problem):
    print('TODO')

# Calls `make clean` on the terminal to clean up makewff binary executable
def clean_up():
    subprocess.call(["make", "clean"])

if __name__ == '__main__':
    run()
