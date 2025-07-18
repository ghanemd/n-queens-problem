import sys
import random

class Variable:
    def __init__(self, i, j):
        """
        Create a new variable containing the row number and the col number.
        """
        self.i = i
        self.j = j

    def __eq__(self, other):
        return self.i == other.i and self.j == other.j 
    
    def __hash__(self):
        return hash((self.i, self.j))
    
    def __str__(self):
        return f"i = {self.i}, j = {self.j}"
    

class NQueensBoard:
    def __init__(self, N):
        self.N = N

        self.height = N
        self.width = N

        self.variables = set()
        for i in range(self.height):
            for j in range(self.width):
                self.variables.add(Variable(i, j))

    def are_neighbors(self, var1, var2):
        """
        Check if two variables are neighbors.
        """
        return var1.i == var2.i or var1.j == var2.j or (abs((var1.j-var2.j)/(var1.i-var2.i)) == 1 or abs((var1.j-var2.j)/(var1.i-var2.i)) == -1)
    
    def neighbors(self, var):
        """
        Return a set of the neighbors of var.
        """
        return set(
            v for v in self.variables
            if v != var and self.are_neighbors(v, var)
        )


class NQueensSolver:
    def __init__(self, nqueens_board):
        self.nqueens_board = nqueens_board
        self.domains = {
            var: {True, False}
            for var in self.nqueens_board.variables
        }

    def save(self,assignement, file_name):      # Missing implementation using the pillow library
        pass

    def solve(self):
        """
        Solve the CSP.
        """
        return self.backtrack(dict())

    def backtrack(self, assignement):
        """
        Using Backtracking Search, take as input a partial assignment
        and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to a truth value (False or True).

        If no assignment is possible, return None.
        """
        if self.assignement_complete(assignement):
            return assignement
        var = self.select_unassigned_variable(assignement)
        for val in self.domains[var]:
            assignement[var] = val
            if self.assignement_consistent(assignement):
                result = self.backtrack(assignement)
                if result is not None:
                    return result
            del assignement[var]
        return None

    def select_unassigned_variable(self, assignement):     
        """
        Return an unassigned variable randomly. 
        """
        return random.choice([var for var in self.domains if var not in assignement])

    def assignement_complete(self, assignement):
        """
        Check if all the variables are assigned.
        """
        return len(assignement) == len(self.domains)

    def assignement_consistent(self, assignement):
        """
        Check if the constraints in a given assignement are satisfied.
        """
        for var in assignement:
            if assignement[var] and any(assignement[v] for v in self.nqueens_board.neighbors(var)):
                return False
        return True


def main():

    # Check command-line arguments
    if len(sys.argv) == 3 and (sys.argv[1] == "-n" or sys.argv[1] == "--number"):
        try:
            N = int(sys.argv[2])
        except ValueError:
            sys.exit("Invalid Usage")
        else:
            nqueens_board = NQueensBoard(N)
            nqueens_solver = NQueensSolver(nqueens_board)
            assignements = nqueens_solver.solve()
            if not assignements:
                print("No solution")
            else:
                pass
    else:
        sys.exit("Invalid Usage")

    
if __name__ == "__main__":
    main()