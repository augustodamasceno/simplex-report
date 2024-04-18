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


import utils

DEFAULT_FILE = 'problem.txt'


def simplex():
    pass


if __name__ == "__main__":
    print(f'Simplex Report Version {__version__}\n' +
          f'Reading the linear problem in the file {DEFAULT_FILE}')

    objective, constraint_vars, constraint_consts = utils.read_problem(filename=DEFAULT_FILE)
    utils.problem_summary(objective=objective,
                          constraint_vars=constraint_vars,
                          constraint_consts=constraint_consts)
