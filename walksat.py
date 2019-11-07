import matplotlib.pyplot as plt
import csv
import sys
import math
from random import *
import subprocess

def run():
    init_problem_generator()
    generate_problems(20)
    clean_up()

# Calls `make` on the terminal to produce the makewff binary executable
def init_problem_generator():
    subprocess.call(["make"])

# Calls makewff to generate a 3-SAT problem with 20 variables and the given
# number of clauses
def generate_problems(num_clauses):
    test = subprocess.check_output(["./makewff", "-cnf", "3", "20", str(num_clauses)])
    print(test.decode('utf-8').split("\n")[2:])

# Calls `make clean` on the terminal to clean up makewff binary executable
def clean_up():
    subprocess.call(["make", "clean"])

if __name__ == '__main__':
    run()
