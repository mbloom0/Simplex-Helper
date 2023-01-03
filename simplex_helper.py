from fractions import Fraction

"""
This script contains functions for performing the simplex algorithm on a matrix of values. The simplex algorithm is
used to solve linear programming problems, which seek to optimize (maximize) the value of a linear objective function subject to
constraints represented by a system of linear inequalities.

This implementation can handle both minimization and maximization problems, as well as problems with fractional coefficients.

The pivot function takes a matrix and pivots about a given row and column. The simplex function applies pivot operations
until the optimal solution is reached. The pretty_print function formats and prints the matrix in a visually appealing
format.

Running the script will prompt the user to enter the matrix row by row, with each element as an integer, or in the form
of a fraction (e.g. 1/2). The user will then be prompted to enter the row and column to pivot on. The resulting matrix
will be printed after each pivot operation, and when the optimal solution is reached, the solution will be printed.

The file can be run from the command line using the command "python simplex_helper.py" from the folder where the script is contained.

@Author Max Bloom
Developed with resources freely provided by OpenAI
"""

def pivot(matrix: list, row: int, col: int) -> list:
    """
    Pivot the matrix about the given row and column.

    Parameters:
    matrix (list): The matrix to pivot.
    
    row (int): The row to pivot about.
    
    col (int): The column to pivot about.

    Returns: 
    list: The pivoted matrix.
    """
    # get pivot value
    pivot = matrix[row][col]

    # handle integer vs fraction division
    if isinstance(pivot, int):
        matrix[row] = [x // pivot if x % pivot == 0 else Fraction(x, pivot) for x in matrix[row]]
    else:
        matrix[row] = [x / pivot for x in matrix[row]]
    
    # apply the pivot operation
    for r in range(len(matrix)):
        if r == row:
            continue
        if isinstance(matrix[r][col], int) and isinstance(matrix[row][col], int):
            matrix[r] = [x - y * (matrix[r][col] // matrix[row][col]) if matrix[r][col] % matrix[row][col] == 0 else x - y * Fraction(matrix[r][col], matrix[row][col]) for x, y in zip(matrix[r], matrix[row])]
        else:
            matrix[r] = [x - y * matrix[r][col] for x, y in zip(matrix[r], matrix[row])]
    
    # Convert Fractions with denominator 1 back into integers
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if isinstance(matrix[i][j], Fraction) and matrix[i][j].denominator == 1:
                matrix[i][j] = matrix[i][j].numerator
    
    return matrix

def simplex(matrix: list) -> list:
    """
    Execute the simplex algorithm on the given matrix.

    Parameters:
    matrix (list): A list of lists containing the elements of the matrix.

    Returns:
    list: The resulting matrix after all pivot operations have been completed.
    """
    while True:
        # Find the column with the most negative coefficient, excluding last column in case of minimization
        col = matrix[-1][:-1].index(min(matrix[-1][:-1]))
        if matrix[-1][col] >= 0:
            return matrix

        # Find the row with the minimum ratio
        row = min(range(len(matrix) - 1), key=lambda x: matrix[x][-1] / matrix[x][col] if matrix[x][col] != 0 else float('inf'))
        if matrix[row][-1] == 0:
            raise ValueError("Linear program is unbounded")

        # Ask the user which row and column to pivot on
        try:
            col = int(input("Enter the column to pivot on: "))
            row = int(input("Enter the row to pivot on: "))
        except ValueError:
            print("Please enter an integer value for the pivot column and pivot row")
        
        # Perform the pivot operation
        try:
            matrix = pivot(matrix, row, col)
            print("New matrix after pivot operation: ")
            pretty_print(matrix)
        except ZeroDivisionError:
            print("Cannot pivot on an entry with a value of zero (division by zero error)")

def pretty_print(matrix:list) -> None:
    """
    Print the matrix in a visually appealing format with aligned columns.

    Parameters:
    matrix (list): The matrix to be printed.

    Returns:
    None: The function has the side effect of printing the matrix to the console.
    """
    # Find the maximum number of characters in any element in the matrix for padding purposes
    max_chars = 0
    for row in matrix:
        for x in row:
            if isinstance(x, Fraction):
                num_chars = len(f"{x.numerator}") + len(f"{x.denominator}") + 1
            else:
                num_chars = len(str(int(x)))
            max_chars = max(max_chars, num_chars)
    
    # Print each row with properly aligned columns
    for row in matrix:
        formatted_row = []
        for x in row:
            if isinstance(x, Fraction):
                formatted_x = f"{x.numerator}" + "/" + f"{x.denominator}"
            else:
                formatted_x = str(int(x))
            # Add padding to align the columns
            formatted_row.append(formatted_x.rjust(max_chars))
        print(" ".join(formatted_row))

def main():
    # Read the matrix from the user
    print("Welcome to the simplex helper software! I'm here to assist you with solving linear programming (maximization) problems using the simplex method.")
    print("Please note that for pivot operations, the row and column indices to pivot on start at 0, not 1.")
    print("Please enter the matrix row by row, with each element as an integer, or in the form 'x/y' where x and y are integers:")

    #get user input
    matrix = []
    while True:
        row = input().strip()
        if not row:
            break

        new_row = []
        for x in row.split():
            #handle fraction vs integer input
            if eval(x) == int(x): 
                new_row.append(int(x))
            else:
                new_row.append(Fraction(x))
        matrix.append(new_row)
    
    # Solve the linear program
    result = simplex(matrix)

    # Print the result
    print("Optimal solution:")
    #psedocode: for column columns except the last one
    #   for that column if it is a column of the identity matrix, print the value of the last column with the row associated with the row with the 1 in it
    #   if the column is not the identity matrix, the value is 0
    for i in range(len(result[0]) - 1):
        try:
            row = [x[i] for x in result].index(1)
            print(f"x{i} = {result[row][-1]}")
        except:
            print(f"x{i} = 0")

    print(f"Optimal (maximum) value of objective function: {result[-1][-1]}")

if __name__ == "__main__":
    main()