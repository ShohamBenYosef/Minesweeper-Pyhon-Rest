class Cell(object):
    """
        Represents a single cell on the Minesweeper board.
        """
    def __init__(self):
        """
                Initializes a hidden, non-mine, non-flagged cell with zero neighboring mines.
                """
        self.is_mine = False
        self.is_visible = False
        self.is_flag = False
        self.neighbor_mines = 0


    def reveal(self):
        """
               Reveals the cell (makes it visible).
               """
        self.is_visible = True

    #
    def toggle_flag(self):
        """
                Toggles the flagged status of the cell (on/off).
                """
        self.is_flag = not self.is_flag

