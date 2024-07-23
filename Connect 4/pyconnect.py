#imports
import pygame
import numpy
import math
import pygame.examples
import pygame.examples.stars
import pygame.locals
import random
import time

# Define constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
CELL_SIZE = 100
BOARD_ROWS = 6
BOARD_COLS = 7
BOARD_MARGIN = 50
TOP_MARGIN = 100

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

# Buttons
buttonVs = pygame.Rect(WINDOW_WIDTH * 0.3 -100, WINDOW_HEIGHT * 0.4, 200, 100)
buttonBot = pygame.Rect(WINDOW_WIDTH * 0.7 -100, WINDOW_HEIGHT * 0.4, 200, 100)

# Define matrix for board logic
boardMatrix = numpy.zeros((BOARD_ROWS,BOARD_COLS))
#turnColor = RED


def switch_turn(turnColor):
    #global turnColor
    turnColor = YELLOW if turnColor == RED else RED

def draw_options(screen):
    mouse_pos = pygame.mouse.get_pos()
    screen.fill(WHITE)
    font = pygame.font.SysFont('Calibri', 24)
    
    buttonRGB = (200,200,200) if buttonVs.collidepoint(mouse_pos) else (230,230,230)
    pygame.draw.rect(screen, buttonRGB, buttonVs)
    text1 = font.render('VS Player', True, (0,0,0))
    screen.blit(text1, text1.get_rect(center=(WINDOW_WIDTH * 0.3, WINDOW_HEIGHT * 0.4 + 50)))

    buttonRGB = (200,200,200) if buttonBot.collidepoint(mouse_pos) else (230,230,230)
    pygame.draw.rect(screen, buttonRGB, buttonBot)
    text2 = font.render('VS Bot', True, (0,0,0))
    screen.blit(text2, text2.get_rect(center=(WINDOW_WIDTH * 0.7, WINDOW_HEIGHT * 0.4 + 50)))

def check_click():
    mouse_pos = pygame.mouse.get_pos()

    if buttonVs.collidepoint(mouse_pos):
        return 1

    if buttonBot.collidepoint(mouse_pos):
        return 2
    
    return 0

def draw_board(screen, winner, turnColor):
    # Fill the background
    screen.fill(WHITE)

    # Current player color
    curColor = "Yellow" if turnColor == YELLOW else "Red"

    # Draw the board
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            pygame.draw.rect(screen, BLUE, (col*CELL_SIZE + BOARD_MARGIN, row*CELL_SIZE + BOARD_MARGIN + TOP_MARGIN, CELL_SIZE, CELL_SIZE))
            currColor = WHITE
            if boardMatrix[row][col] == 1:
                currColor = YELLOW
            elif boardMatrix[row][col] == 2:
                currColor = RED
            
            pygame.draw.circle(screen, currColor, (int(col*CELL_SIZE + CELL_SIZE/2 + BOARD_MARGIN), int(row*CELL_SIZE + CELL_SIZE/2 + BOARD_MARGIN + TOP_MARGIN)), int(CELL_SIZE/2 - 5))

    if winner == 0:
        # Draw arrow pointing to which column is active using mouse position
        mouse_x, y = pygame.mouse.get_pos()
        col = max(min(math.floor((mouse_x - BOARD_MARGIN) / CELL_SIZE),6),0)

        triangle_points = [(col * CELL_SIZE + CELL_SIZE / 2 + BOARD_MARGIN, BOARD_MARGIN + TOP_MARGIN),
                           (col * CELL_SIZE + BOARD_MARGIN, (TOP_MARGIN)),
                           ((col + 1) * CELL_SIZE + BOARD_MARGIN, (TOP_MARGIN))]
    
        pygame.draw.polygon(screen, BLACK, triangle_points)

        # Display whose turn it is
        font = pygame.font.SysFont('Calibri', 24)
        turnText = font.render(curColor + "'s turn.", True, (0,0,0), (255,255,255))
        screen.blit(turnText, turnText.get_rect(center=(WINDOW_WIDTH/2, BOARD_MARGIN)))
    
    else:
        font = pygame.font.SysFont('Calibri', 24)
        text = []

        # Display winner if winner is not false, else tie
        if winner == 1:
            text.append(font.render(curColor + ' has won!', True, (0,0,0), (255,255,255)))
        else:
            text.append(font.render('Game is a tie.', True, (0,0,0), (255,255,255)))

        text.append(font.render('Press ''R'' to restart.', True, (0,0,0), (255,255,255)))
        # Loop blit to display multiple lines
        for line in range(len(text)):
            textBox = text[line].get_rect(center=(WINDOW_WIDTH/2, 100 + line * 50))
            screen.blit(text[line], textBox)
        
       
def drop_piece(col, turnColor, board=None):
    result = None
    tempBoard = board if isinstance(board, numpy.ndarray) else boardMatrix

    # if mouse position outside column range then do nothing
    if not (col >= 0 and col <= 6):
        return
    
    # Find first open slot to drop piece starting from the bottom of the board
    for row in range(BOARD_ROWS):
        temp_rows = BOARD_ROWS - 1
        if tempBoard[temp_rows-row, col] == 0:
            tempBoard[temp_rows-row, col] = 1 if turnColor == YELLOW else 2
            result = [temp_rows-row,col]
            break

    # Return true if a piece was dropped, false if the column was full
    return result

def horizontal_check(num, board):
    for col in range(BOARD_COLS-3):
        for row in range(BOARD_ROWS):
            if board[row][col] == num and board[row][col+1] == num and board[row][col+2] == num and board[row][col+3] == num:
                return True

    return False


def vertical_check(num, board):
    for col in range(BOARD_COLS):
        for row in range(BOARD_ROWS-3):
            if board[row][col] == num and board[row+1][col] == num and board[row+2][col] == num and board[row+3][col] == num:
                return True

    return False

def diagonal_check(num, board):
    for col in range(BOARD_COLS-3):
        for row in range(BOARD_ROWS-3):
            if board[row][col] == num and board[row+1][col+1] == num and board[row+2][col+2] == num and board[row+3][col+3] == num:
                return True
            
    for col in range(BOARD_COLS-3):
        for row in range(3, BOARD_ROWS):
            if board[row][col] == num and board[row-1][col+1] == num and board[row-2][col+2] == num and board[row-3][col+3] == num:
                return True
    
    return False

def check_win(turnColor, board = None):
    tempBoard = board if isinstance(board, numpy.ndarray) else boardMatrix
    # get number to check for in matrix
    num = 1 if turnColor == YELLOW else 2

    # Check Horizontal
    if horizontal_check(num, tempBoard):
        return 1
    # Check Vertical
    if vertical_check(num, tempBoard):
        return 1
    # Check Diagonal
    if diagonal_check(num, tempBoard):
        return 1
    
    return 0

#

def bot_easy():
    return random.randint(0,BOARD_COLS)

# Create function for bot with logic #TODO

