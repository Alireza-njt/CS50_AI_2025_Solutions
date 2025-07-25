# name : Alireza Nejati
# gmail address : alirezanejatiz27@gmail.com
# github ID : Alireza-njt
# last submit : Thursday, July 3, 2025 4:11 AM +0330


# import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count:
            return self.cells
        elif len(self.cells) == 0:
            return set()
        else:
            return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        elif len(self.cells) == self.count:
            return set()
        else:
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.count = self.count - 1
            self.cells.remove(cell)
        else:
            pass

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)
        else:
            pass


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        self.moves_made.add(cell)  # Request number 1
        self.mark_safe(cell)  # Request number 2
        '''_____________________________________________________________________________________'''
        # START : Request number 3
        cell_neighbors_list = []
        cell_i, cell_j = cell
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i == 0 and j == 0:
                    pass
                else:
                    new_i = i + cell_i
                    new_j = j + cell_j
                    if (new_i >= 0 and new_i < self.height and new_j >= 0 and new_j < self.width):
                        if ((new_i, new_j) not in self.mines and (new_i, new_j) not in self.safes):
                            cell_neighbors_list.append((new_i, new_j))
                        elif ((new_i, new_j) in self.mines):
                            count = count - 1
        new_sentence = Sentence(cell_neighbors_list, count)
        self.knowledge.append(new_sentence)
        # FINISH : Request number 3
        '''_____________________________________________________________________________________'''
        # START : Request number 4 & 5
        update_knowledge_sw = True
        while update_knowledge_sw:
            update_knowledge_sw = False
            new_knowledge = []

            for sentence in self.knowledge:
                known_mines = sentence.known_mines()
                known_safes = sentence.known_safes()

                if known_mines:
                    update_knowledge_sw = True
                    for cell in known_mines.copy():
                        self.mark_mine(cell)

                if known_safes:
                    update_knowledge_sw = True
                    for cell in known_safes.copy():
                        self.mark_safe(cell)

            self.knowledge = [s for s in self.knowledge if s.cells]

            for sentence1 in self.knowledge:
                for sentence2 in self.knowledge:
                    if sentence1 != sentence2 and sentence1.cells.issubset(sentence2.cells):
                        new_sentence = Sentence(sentence2.cells - sentence1.cells,
                                                sentence2.count - sentence1.count)
                        if new_sentence not in self.knowledge and new_sentence not in new_knowledge:
                            new_knowledge.append(new_sentence)
                            update_knowledge_sw = True

            self.knowledge.extend(new_knowledge)
        # FINISH : Request number 4 & 5
        '''_____________________________________________________________________________________'''

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """

        for cell in self.safes:
            if cell not in self.moves_made:
                return cell

        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        random_move = (2025, 2025)
        k = 0
        for k in range(self.height*self.width):
            i = random.randint(0, self.height-1)
            j = random.randint(0, self.width-1)
            random_move = (i, j)
            if random_move not in self.mines:
                return None
        if k != self.height*self.width:
            return random_move
        else:
            return None
