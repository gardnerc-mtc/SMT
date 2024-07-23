# Import connect 4 file
import pygame
import sys
import numpy
import time
from pyconnect import *

# Run main loop 
def main():
    pygame.init()
    
    # Set up some variables for the window
    window_size = (WINDOW_WIDTH, WINDOW_HEIGHT)
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Pygame Connect 4")
    winner = 0 # 0 - no winner, 1 - winner, 2 - tie
    gamemode = 1 # 1 PvP, 2 PvAI
    turnColor = RED

    # Main game loop
    while True:
        result = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if gamemode != 0 and winner == 0:
                if event.type == pygame.MOUSEBUTTONUP and winner == 0:
                    # Get mouse pos and determine col
                    print("Do nothing")
                    

            if event.type == pygame.KEYUP:
                if event.key == pygame.locals.K_r and winner != 0:
                    print ("Do nothing")

                elif event.key == pygame.locals.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        if result != None:
            print("Do nothing")                  

        draw_board(screen, winner, turnColor)

        # Update the display
        pygame.display.update()

        # Limit loops per second
        clock = time.perf_counter() * 60
        sleep = int(clock) + 1 - clock
        time.sleep(sleep/60)

if __name__ == "__main__":
    main()
