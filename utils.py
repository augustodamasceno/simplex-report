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


def read_problem(filename: str):
    """

    :param filename:
    :return:
    """
    assert isinstance(filename, str), 'filename must be a str'

    status = True
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"Error: The file '{filename}' does not exist.")
        status = False
    except PermissionError:
        print(f"Error: You do not have the necessary permissions to read the file '{filename}'")
        status = False
    except IOError:
        print(f"Error: An I/O error occurred while reading the file '{filename}'")
        status = False
    except Exception as e:
        print(f"An unexpected error occurred while trying to read the file '{filename}': {e}")
        status = False

    if status:
        objective = list(map(float, lines[0].strip().split()))
        constraint_vars = []
        constraint_consts = []

        for line in lines[1:]:
            parts = list(map(float, line.strip().split()))
            constraint_vars.append(parts[:-1])
            constraint_consts.append(parts[-1])
    else:
        objective = None
        constraint_vars = None
        constraint_consts = None

    return objective, constraint_vars, constraint_consts


def array2poly(poly_arr):
    """

    :param poly_arr:
    :return:
    """
    poly_str = str(np.poly1d(poly_arr))
    just_poly = poly_str.split('\n')[1]
    return just_poly


def problem_summary(objective, constraint_vars, constraint_consts):
    """

    :param objective:
    :param constraint_vars:
    :param constraint_consts:
    :return:
    """
    print(f"Objective Function: {array2poly(objective)}")
    print(f'Constraints')
    for index, cvar in enumerate(constraint_vars):
        print(f"{array2poly(cvar)} <= {array2poly(constraint_consts[index])}")


if __name__ == "__main__":
    pass
