# name : Alireza Nejati
# gmail address : alirezanejatiz27@gmail.com
# github ID : Alireza-njt
# last submit : Saturday, July 12, 2025 1:45 AM +0430


import sys

from crossword import *
from collections import deque  # added by me !!!!!!


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for variable_object in self.domains.keys():
            variable_object_len = variable_object.length
            self_domains_v_list = list(self.domains[variable_object])
            for x in self_domains_v_list:
                if len(x) != variable_object_len:
                    self.domains[variable_object].remove(x)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        overlap = self.crossword.overlaps.get((x, y)) or self.crossword.overlaps.get((y, x))
        if overlap is None:
            return False

        i, j = overlap if (x, y) in self.crossword.overlaps else (overlap[1], overlap[0])
        x_values = list(self.domains[x])
        result = False

        for vx in x_values:
            compatible = any(
                vx[i] == vy[j]
                for vy in self.domains[y]
            )
            if not compatible:
                self.domains[x].remove(vx)
                result = True

        return result

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        queue = 2025
        if arcs is not None:
            queue = deque(arcs)
        else:
            queue = deque()
            for keys in self.domains.keys():
                keys_neighbors = list(self.crossword.neighbors(keys))
                for n in keys_neighbors:
                    queue.append((n, keys))
        while len(queue) != 0:
            x, y = queue.popleft()
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
                for z in self.crossword.neighbors(x):
                    if (z != y):
                        queue.append((z, x))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for v in self.crossword.variables:
            if v not in assignment.keys():
                return False
            if assignment[v] not in self.crossword.words:
                return False
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        for v in assignment:
            if v.length != len(assignment[v]):
                return False
            for neighbor in self.crossword.neighbors(v):
                if neighbor in assignment:
                    i, j = self.crossword.overlaps[v, neighbor]
                    if assignment[v][i] != assignment[neighbor][j]:
                        return False
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        var_words = self.domains[var]
        word_conflicts = dict()
        old_neighbors = self.crossword.neighbors(var)
        neighbors = old_neighbors.copy()
        for n in old_neighbors:
            if n in assignment:
                neighbors.remove(n)
        for word in var_words:
            number = 0
            for n in neighbors:
                for word2 in self.domains[n]:
                    overlap = self.crossword.overlaps[var, n]
                    if overlap:
                        overlap_letter_index_for_word, overlap_letter_index_for_word2 = overlap
                        if word[overlap_letter_index_for_word] != word2[overlap_letter_index_for_word2]:
                            number += 1
            word_conflicts[word] = number
        return sorted(word_conflicts.keys(), key=lambda x: word_conflicts[x])

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        results = []
        for v in self.domains:
            if v not in assignment:
                results.append((v, len(self.domains[v]), len(self.crossword.neighbors(v))))
        if results:
            results.sort(key=lambda x: (x[1], -x[2]))
            return results[0][0]
        return None

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        variable = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(variable, assignment):
            assignment[variable] = value
            if self.consistent(assignment):
                result = self.backtrack(assignment)
                if result:
                    return result
                assignment.pop(variable, None)
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
