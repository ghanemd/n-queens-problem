import sys
import random
from PIL import Image, ImageDraw

class Variable:
    def __init__(self, row):
        """
        Create a new variable containing the row number.
        """
        self.row = row

    def __eq__(self, other):
        return self.row == other.row
    
    def __hash__(self):
        return hash(self.row)
    
    def __str__(self):
        return f"row = {self.row}"
    

class NQueensBoard:
    def __init__(self, N):
        self.N = N
        self.variables = {
            Variable(i) for i in range(self.N)
        }


class NQueensSolver:
    def __init__(self, nqueens_board):
        self.nqueens_board = nqueens_board
        self.domains = {
            var: set(range(self.nqueens_board.N))
            for var in self.nqueens_board.variables
        }

    def save(self,assignment, file_name):      # Missing implementation using the pillow library
        """
        Save the assignment to an image file.
        """
        cell_size = 50
        cell_border = 2
        img = Image.new(
            "RGBA",
            (self.nqueens_board.N * cell_size,
             self.nqueens_board.N * cell_size),
            "black"
        )
        queen = Image.open("queen.png").resize(
            (cell_size, cell_size)
        )
        draw = ImageDraw.Draw(img)
        for i in range(self.nqueens_board.N):
            for j in range(self.nqueens_board.N):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]

                if i % 2 == j % 2 :
                    draw.rectangle(rect, fill="green")
                else:
                    draw.rectangle(rect, fill="white")

                if self.queen_in_cell(assignment, i, j):
                    img.paste(queen, rect[0], queen)
                                
        img.save(file_name)

    def queen_in_cell(self, assignment, i, j):
        """
        Check if there is a queen in the cell (i, j).
        """
        for var in assignment:
            if var.row == i and assignment[var] == j:
                return True
        return False

    def solve(self):
        """
        Solve the CSP.
        """
        return self.backtrack(dict())

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment
        and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to a truth value (False or True).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        for val in self.domains[var]:
            assignment[var] = val
            if self.assignment_consistent(assignment):
                result = self.backtrack(assignment)
                if result is not None:
                    return result
            del assignment[var]
        return None

    def select_unassigned_variable(self, assignment):     
        """
        Return an unassigned variable randomly. 
        """
        return random.choice([var for var in self.domains if var not in assignment])

    def assignment_complete(self, assignment):
        """
        Check if all the variables are assigned.
        """
        return len(assignment) == self.nqueens_board.N

    def assignment_consistent(self, assignment):
        """
        Check if the constraints in a given assignement are satisfied.
        """
        for var1 in assignment:
            for var2 in assignment:
                
                if var1 == var2:
                    continue
                if assignment[var1] == assignment[var2]:
                    return False
                if abs(var1.row - var2.row) == abs(assignment[var1] - assignment[var2]):
                    return False
                
        return True


def main():

    # Check command-line arguments
    if len(sys.argv) == 4 and (sys.argv[1] == "-n" or sys.argv[1] == "--number"):

        try:
            N = int(sys.argv[2])
        except ValueError:
            sys.exit("Invalid Usage")
        else:
            nqueens_board = NQueensBoard(N)
            nqueens_solver = NQueensSolver(nqueens_board)
            assignment = nqueens_solver.solve()
            output = sys.argv[3]
            if not assignment:
                print("No solution")
            else:
                nqueens_solver.save(assignment, output)
                
    else:
        sys.exit("Invalid Usage")

    
if __name__ == "__main__":
    main()