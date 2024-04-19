# simplex-report
Simplex Report is designed to solve linear optimization problems using the Simplex algorithm.  
It provides detailed reports on the optimization process, making it ideal for academic and professional use.  

> Copyright (c) 2024, Augusto Damasceno, Elayne Carvalho, N1LB13, pedrojot4, wtnhrr  
> All rights reserved.   
> SPDX-License-Identifier: BSD-2-Clause

# Install
```bash
pip install -r requirements.txt
```

# Run
- The simplex.py execution reads the linear problem described in the Input File 'problem.txt'.  

## Input File Structure

The input file should consist of text where:
- The first line contains the coefficients of the objective function.
- Subsequent lines represent the constraints.

### Detailed Breakdown

**Objective Function:**
- The first line must list the coefficients of the variables in the objective function, separated by spaces.
  - Example: `3 4 5` which represents the objective function `3x + 4y + 5z`.

**Constraints:**
- Each of the following lines should represent a single constraint.
- Constraint lines must list the coefficients for each variable followed by the constant term, all separated by spaces.
  - Example: `1 0 3 30` which represents the constraint `1x + 0y + 3z <= 30`.

### Example Input File

- The objective is to maximize `3x + 4y + 5z`.
- Subject to constraints:
  - `1x + 0y + 3z <= 30`
  - `0y + 2y + 1z <= 40`
  - `1x + 1y + 0z <= 10`

### Notes
- Ensure there are no extra spaces or lines in your input file.
- The number of spaces between coefficients on the same line must be consistent.
- The script currently supports "less than or equal to" (`<=`) constraints. If your model requires different types of constraints, you may need to adjust the script accordingly.

By following this input format, you can ensure that your linear programming problems are correctly read and processed by the script.

## Screenshots for the Input File 'problem2.txt'
![problem2_1.png](img%2Fproblem2_1.png)
![problem2_2.png](img%2Fproblem2_2.png)
![problem2_3.png](img%2Fproblem2_3.png)