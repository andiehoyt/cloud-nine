from sympy import symbols, Eq, sqrt, solve

# Define the variable
x = symbols('x')

# Define the equation
equation = Eq(2 / sqrt(x + 4), sqrt(x + 1))

# Solve the equation
solutions = solve(equation, x)
solutions
