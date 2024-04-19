# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""Simplex Report (https://github.com/augustodamasceno/simplex-report)

Simplex Main File.

Copyright (c) 2024, Augusto Damasceno, Elayne Carvalho, N1LB13, pedrojot4, wtnhrr.
All rights reserved.
"""

__author__ = "Augusto Damasceno, Elayne Carvalho, N1LB13, pedrojot4, wtnhrr"
__version__ = "1.0"
__copyright__ = "Copyright (c) 2024, Augusto Damasceno, Elayne Carvalho, N1LB13, pedrojot4, wtnhrr."
__license__ = "All rights reserved"


import numpy as np
from tabulate import tabulate

import utils

DEFAULT_FILE = 'problem.txt'
DEFAULT_FILE_2 = 'problem2.txt'


class Simplex:
    def __init__(self, problem_filename: str, minimization: bool = True,  **kwargs):
        self.description = f'Simplex Problem from {problem_filename}'
        self.minimization = minimization
        self.max_iterations = 300
        self.seed = int(np.random.randint(2**23))
        self.report_mode = True

        for key, value in kwargs.items():
            if key in self.__dict__ and isinstance(value, type(self.__dict__[key])):
                self.__dict__[key] = value

        self.objective, self.constraint_vars, self.constraint_consts = utils.read_problem(filename=problem_filename)
        self.solved = False
        self.solution_coefs = []
        self.solution = np.nan
        self.basic = []
        self.non_basic = []
        self.num_variables = len(self.objective)
        self.num_constraints = len(self.constraint_consts)
        self.tableau = None
        self.iteration = 1
        self.unbounded = False
        np.random.seed(self.seed)

        self.make_tableau()

    def __repr__(self):
        the_summary = (self.description
                       + '\n'
                       + utils.problem_summary(self.objective, self.constraint_vars, self.constraint_consts)
                       + '\n')
        if self.solved:
            the_summary += (utils.array2poly(self.solution_coefs)
                            + '\n'
                            + f"Solution {self.solution:.2f}")

        return the_summary

    def make_tableau(self):
        tableau = None
        if self.minimization:
            num_columns = self.num_variables + self.num_constraints + 2
            tableau = np.zeros((self.num_constraints + 1, num_columns))

            # Objective Function
            tableau[-1, :self.num_variables] = np.array(self.objective)

            # Constraints Vars
            tableau[:self.num_constraints, :self.num_variables] = np.array(self.constraint_vars)

            # Constraints Constants
            tableau[:-1, -1] = np.array(self.constraint_consts)

            # Eye Matrix
            tableau[:, self.num_variables:-1] = np.eye(self.num_constraints+1)

        self.tableau = tableau

    def solve(self):
        print('Starting the Simplex Algorithm')
        while not self.stopping_criteria():
            if self.report_mode:
                print('+'*99)
                print(f'Iteration {self.iteration}\nTableau:\n')
                print(self.tableu_repr())
            pivot = self.get_pivot()
            var_const_div = self.tableau[:, -1] / self.tableau[:, pivot]
            inf_mask = np.isinf(var_const_div)
            var_const_div[inf_mask] = 0
            div_positive_nonzero = var_const_div[var_const_div > 0]
            if len(div_positive_nonzero) == 0:
                self.unbounded = True
                break
            best_value_div = np.nanmin(div_positive_nonzero)
            options = np.where(var_const_div == best_value_div)[0]
            best_constraint_index = np.random.choice(options)

            indicator = self.tableau[best_constraint_index, pivot]
            self.tableau[best_constraint_index, :] /= indicator

            if self.report_mode:
                print(f'Pivot {pivot+1}\n'
                      + f'Choose equation {best_constraint_index+1} as pivot from options {options+1}\n'
                      + f'The indicator is located on ({best_constraint_index+1},{pivot+1})')

            for constraint_row in range(self.num_constraints+1):
                if constraint_row != best_constraint_index:
                    multiplier = self.tableau[constraint_row, pivot] / self.tableau[best_constraint_index, pivot]
                    self.tableau[constraint_row, :] -= multiplier * self.tableau[best_constraint_index, :]
                    if self.report_mode:
                        print(f"Making the variable of the equation {constraint_row+1} zero")
                        print(f"Equation_{constraint_row+1} = Equation_{constraint_row+1} - {multiplier} "
                              + f"* Equation_{best_constraint_index+1}")

            self.solved = np.sum(self.tableau[-1, :] >= 0) == self.tableau.shape[1]
            if not self.solved and self.report_mode:
                print('The tableau still has negative values on the last row. No solution has been found yet.')
            if self.solved and self.report_mode:
                print('The tableau has no negative values on the last row. A solution has been found!')

            self.iteration += 1

        self.solution_coefs = []
        self.basic = []
        basic_row_index_nonzero = []
        for column in range(self.num_variables + self.num_constraints + 1):
            if np.sum(self.tableau[:-1, column] != 0) == 1:
                row = np.where(self.tableau[:-1, column] != 0)[0][0]
                self.basic.append(1)
                basic_row_index_nonzero.append(row)
            else:
                self.basic.append(0)
        for index in range(self.num_variables):
            if self.basic[index] == 1:
                self.solution_coefs.append(self.tableau[basic_row_index_nonzero[index], -1])
            else:
                self.solution_coefs.append(0)
        self.solution = self.tableau[-1, -1]
        if self.report_mode:
            print('Final Tableau:\n')
            print(self.tableu_repr())
            if self.solved:
                print(f'Solution: {utils.array2poly(self.solution_coefs)} = {self.solution}')
            else:
                print('Not Solved. Terminated by number of iterations or Simplex cannot continue.')


    def tableu_repr(self):
        tableu_str = ''
        if self.tableau is not None:
            var_labels = [f'X{index+1}'for index in range(len(self.constraint_vars)+1)]
            slack_labels = [f'S{index+1}' for index in range(len(self.constraint_vars)+1)]
            constant_label = [str(const) for const in self.constraint_consts]
            headers = var_labels + slack_labels + ['b']
            tableu_str = tabulate(self.tableau, headers=headers, tablefmt='pipe')

        return tableu_str

    def stopping_criteria(self):
        return (self.iteration > self.max_iterations) or self.solved or self.unbounded

    def get_pivot(self):
        return np.argmin(self.tableau[-1, :])


if __name__ == "__main__":
    print(f'Simplex Report Version {__version__}\n' +
          f'Reading the linear problem in the file {DEFAULT_FILE}')

    simplex = Simplex(problem_filename=DEFAULT_FILE,
                      seed=42,
                      minimization=True,
                      report_mode=True,
                      description='Trabalho 1')
    simplex.solve()
