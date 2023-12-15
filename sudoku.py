# Imports pygame and other classes/functions
import pygame
from board import Board
from button import Button

if __name__ == "__main__":
    # Initializes the game UI and what shows up when the user starts the game
    pygame.init()
    screen = pygame.display.set_mode((450, 500))
    pygame.display.set_caption("Sudoku")
    clock = pygame.time.Clock()
    image = pygame.transform.scale(pygame.image.load("sudokuback.jpg"), (450, 500))
    running = True
    is_start = True
    is_board = False
    is_lose = False
    is_win = False
    # Creates buttons for the user to press that selects difficulty
    difficulty = None
    welcome_font = pygame.font.SysFont("verdana", 36, True)
    mode_font = pygame.font.SysFont("verdana", 28, True)
    easy_button = Button(50, 320, 100, 40, "EASY")
    medium_button = Button(180, 320, 100, 40, "MEDIUM")
    hard_button = Button(310, 320, 100, 40, "HARD")
    # Creates buttons for the user to reset, restart, or leave
    board_coords = None
    pressed_num = None
    entered_num = None
    sudoku_board = None
    reset_button = Button(30, 460, 90, 35, "RESET")
    restart_button = Button(180, 460, 90, 35, "RESTART")
    exit_button = Button(330, 460, 90, 35, "EXIT")

    game_result_font = pygame.font.SysFont("verdana", 48, True)
    won_button = Button(160, 270, 120, 50, "EXIT")
    won_button.button_font = pygame.font.SysFont("verdana", 20)
    lost_button = Button(160, 270, 120, 50, "RESTART")
    lost_button.button_font = pygame.font.SysFont("verdana", 20)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Quits out of the game
                running = False

            if is_start:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if 50 <= x <= 150 and 320 <= y <= 360:
                        difficulty = 30
                    if 180 <= x <= 280 and 320 <= y <= 360:
                        difficulty = 40
                    if 310 <= x <= 410 and 320 <= y <= 360:
                        difficulty = 50
                    if difficulty:
                        sudoku_board = Board(450, 450, screen, difficulty)
                        is_start = False
                        is_board = True
                        difficulty = None

            if is_board:
                # creates events for if the user clicks something on the board
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if x <= 450 and y <= 450:
                        board_coords = sudoku_board.click(y, x)
                        pressed_num = None
                    else:
                        if 30 <= x <= 120 and 460 <= y <= 490:
                            sudoku_board.reset_to_original()
                            pressed_num = None
                        if 180 <= x <= 270 and 460 <= y <= 495:
                            is_start = True
                            is_board = False
                            board_coords = None
                            pressed_num = None
                            entered_num = None
                            sudoku_board = None
                        if 330 <= x <= 420 and 460 <= y <= 495:
                            running = False
                # Allows the user to navigate squares using number keys
                if event.type == pygame.KEYDOWN:
                    if board_coords:
                        if event.key == pygame.K_UP:
                            board_coords = (board_coords[0] - (board_coords[0] - 1 > -1), board_coords[1])
                        elif event.key == pygame.K_DOWN:
                            board_coords = (board_coords[0] + (board_coords[0] + 1 < 9), board_coords[1])
                        elif event.key == pygame.K_LEFT:
                            board_coords = (board_coords[0], board_coords[1] - (board_coords[1] - 1 > -1))
                        elif event.key == pygame.K_RIGHT:
                            board_coords = (board_coords[0], board_coords[1] + (board_coords[1] + 1 < 9))

                    if event.key == pygame.K_RETURN:
                        entered_num = sudoku_board.selected_cell.sketched_value
                        pressed_num = None

                    if event.key == pygame.K_BACKSPACE:
                        sudoku_board.clear()

                    if "1" <= event.unicode <= "9":
                        pressed_num = event.unicode
                    else:
                        pressed_num = None
            # Ends the game when the user wins
            if is_win:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if 160 <= x <= 280 and 270 <= y <= 320:
                        running = False

            if is_lose:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if 160 <= x <= 280 and 270 <= y <= 320:
                        is_start = True
                        is_board = False
                        is_lose = False
                        board_coords = None
                        pressed_num = None
                        entered_num = None
                        sudoku_board = None

        if is_start:
            # Draws the UI for the start of the program
            screen.blit(image, (0, 0))
            screen.blit(welcome_font.render("Welcome to Sudoku", True, "black", None), (25, 100))
            screen.blit(mode_font.render("Select Game Mode:", True, "black", None), (75, 225))
            easy_button.draw(screen)
            medium_button.draw(screen)
            hard_button.draw(screen)

        elif is_board:
            # Fills the board and draws the squares
            screen.fill("light blue")
            sudoku_board.draw()

            if board_coords:
                sudoku_board.select(*board_coords)

            if pressed_num:
                sudoku_board.sketch(pressed_num)

            if entered_num:
                sudoku_board.place_number(entered_num)
                entered_num = None

            reset_button.draw(screen)
            restart_button.draw(screen)
            exit_button.draw(screen)
            # Grants a win or loss based on the board checks
            if sudoku_board.check_board():
                is_win = True
                is_board = False
            elif sudoku_board.is_full():
                print("USER LOSE")
                is_lose = True
                is_board = False

        elif is_win:
            # Creates the win screen
            screen.blit(image, (0, 0))
            screen.blit(game_result_font.render("Game Won!", True, "black", None), (70, 100))
            won_button.draw(screen)

        elif is_lose:
            # Creates the lose screen
            screen.blit(image, (0, 0))
            screen.blit(game_result_font.render("Game Over :(", True, "black", None), (55, 100))
            lost_button.draw(screen)

        pygame.display.update()

        clock.tick(60)
