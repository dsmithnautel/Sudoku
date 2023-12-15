import pygame
from cell import Cell
import sudoku_generator


class Board:
    def __init__(self, width, height, screen, difficulty):
        self.width = width
        self.height = height
        self.screen = screen
        self.difficulty = difficulty
        self.gen = sudoku_generator.SudokuGenerator(9, difficulty)
        self.gen.fill_values()
        # defines a solved board as the randomly generated board
        self.solved_board = [row[:] for row in self.gen.get_board()]
        self.gen.print_board()
        self.gen.remove_cells()
        self.sudoku = self.gen.get_board()
        self.cell_list = [[Cell(self.sudoku[i][j], i, j, self.screen) for j in range(0, 9)] for i in range(0, 9)]
        self.selected_cell = None

    def draw(self):
        i = 0
        for i in range(0, 9):
            for j in range(0, 9):
                if self.cell_list[i][j].sketched_value:
                    self.cell_list[i][j].draw(True)
                else:
                    self.cell_list[i][j].draw(False)

        for x in range(0, self.width + 1, int(self.width/3)):
            # draws large lines that separate 3x3 cells
            pygame.draw.line(self.screen, (0, 0, 0), (x, 0), (x, self.height), width=3)
            pygame.draw.line(self.screen, (0, 0, 0), (0, x), (self.height, x), width=3)
            i += 1
            for smallX in range(x, int(self.width/3) * i, int(self.width/9)):
                # draws small cells that separate individual cells
                pygame.draw.line(self.screen, (0, 0, 0), (smallX, 0), (smallX, self.height), width=1)
                pygame.draw.line(self.screen, (0, 0, 0), (0, smallX), (self.height, smallX), width=1)

    def select(self, row, col):
        self.selected_cell = self.cell_list[row][col]
        self.selected_cell.draw(False)
        self.selected_cell.draw_select()

    @staticmethod
    def click(x, y):
        return x // 50, y // 50

    def clear(self):
        if (self.selected_cell.value == self.sudoku[self.selected_cell.row][self.selected_cell.col] and
                # function does not execute if the selected cell is already clear
                self.selected_cell.value != 0):
            return
        self.selected_cell.set_cell_value(0)
        self.selected_cell.set_sketched_value(0)

    def sketch(self, value):
        if (self.selected_cell.value == self.sudoku[self.selected_cell.row][self.selected_cell.col] and
                self.selected_cell.value != 0):
            return
        self.selected_cell.set_sketched_value(value)

    def place_number(self, value):
        if (self.selected_cell.value == self.sudoku[self.selected_cell.row][self.selected_cell.col] and
                self.selected_cell.value != 0):
            return
        self.selected_cell.set_sketched_value(None)
        self.selected_cell.set_cell_value(value)
        # draw method is called in order to update the board
        self.selected_cell.draw(False)

    def reset_to_original(self):
        self.cell_list = [[Cell(self.sudoku[i][j], i, j, self.screen) for j in range(0, 9)] for i in range(0, 9)]

    def is_full(self):
        for row in self.cell_list:
            for cell in row:
                if cell.value == 0:
                    return False
        return True

    def check_board(self):
        if self.is_full():
            for i in range(0, 9):
                for j in range(0, 9):
                    # checks if every individual tile is the intended value by iterating through each cell using nested for loops
                    if int(self.cell_list[i][j].value) != int(self.solved_board[i][j]):
                        return False
            return True
