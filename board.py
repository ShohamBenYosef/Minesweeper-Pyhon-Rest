import random
import cell


class Board(object):
    """
        Represents the Minesweeper game board.
    """
    def __init__(self, width, height, num_of_mines):
        """
            Initialize the board with dimensions and mine count.

            Args:
                width (int): Number of columns.
                height (int): Number of rows.
                num_of_mines (int): Number of mines to place.
        """
        self.width = width
        self.height = height
        self.num_of_mines = num_of_mines
        self.grid = [[cell.Cell() for _ in range(self.width)] for _ in range(self.height)]
        self.game_over = False


    def generate_board(self):
        """
            Place mines and calculate the number of neighboring mines for each cell.
        """
        self.places_mines()
        self.calculate_neighbor_mines()



    def calculate_neighbor_mines(self):
        """
            For each non-mine cell, count how many mines surround it and store the count.
        """
        for y in range(self.height):
            for x in range(self.width):

                if self.grid[y][x].is_mine:
                    continue

                count = 0
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx == 0 and dy == 0:
                            continue
                        nx = x + dx
                        ny = y + dy

                        if 0 <= nx < self.width and 0 <= ny < self.height:
                            if self.grid[ny][nx].is_mine:
                                count += 1

                self.grid[y][x].neighbor_mines = count



    def places_mines(self):
        """
                Randomly place the specified number of mines on the board.
                """
        mines_placed = 0

        while mines_placed < self.num_of_mines:

            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)

            if not self.grid[y][x].is_mine:
                self.grid[y][x].is_mine = True
                mines_placed += 1



    def reveal_cell(self, x, y):
        """
                Reveal a cell and recursively reveal neighbors if the cell has no neighboring mines.

                Args:
                    x (int): X coordinate.
                    y (int): Y coordinate.
                """
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return

        elif self.grid[y][x].is_visible or self.grid[y][x].is_flag:
            return

        self.grid[y][x].reveal()

        if self.grid[y][x].is_mine:
            self.game_over = True
            return

        if self.grid[y][x].neighbor_mines > 0:
            return

        # Recursively reveal neighboring cells
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx = x + dx
                ny = y + dy
                self.reveal_cell(nx, ny)



    def is_won(self):
        """
                Check if all non-mine cells have been revealed.

                Returns:
                    bool: True if the player has won, False otherwise.
                """
        for y in range(self.height):
            for x in range(self.width):
                if not self.grid[y][x].is_visible and not self.grid[y][x].is_mine:
                    return False
        return True



    def toggle_flag(self, x, y):
        """
                Toggle a flag on the given cell.

                Args:
                    x (int): X coordinate.
                    y (int): Y coordinate.
                """
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            print("Invalid coordinate")
            return

        elif self.grid[y][x].is_visible:
            return

        else:
            self.grid[y][x].toggle_flag()

