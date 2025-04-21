'''
Final Project: Sliding Puzzle

Description: A sliding game puzzle with options for shuffling, solving, 3x3 grids, 4x4 grids, 5x5 grids, and one or two surprises

Developer Name(s): Muhammad Conn

Date: 05/21/2024

Resources used:
https://www.pygame.org/docs/
https://www.instructables.com/Making-Slide-Puzzle-With-Python/
https://www.youtube.com/watch?v=DVNxN7Imr2s&list=PLOcNsDskpOqpKhkN6tLId128o0vFWWauV
https://en.wikipedia.org/wiki/Parity_of_a_permutation
https://puzzling.stackexchange.com/questions/118080/possible-parity-for-sliding-puzzle
'''
##########################################
# IMPORTS:
#   modules needed for program
##########################################

import pygame
import random

########################################
# Variable setup
########################################

tile_size = 80  # size of the tiles
origin = 50  # where the start of the board will be drawn

# length and height of the board window
window_width = 1024
window_height = 600

fps = 60  # frames per second value

blank = None

# Color variables

black = (0, 0, 0)

white = (255, 255, 255)

dark_blue = (3, 54, 73)

green = (141, 220, 164)

red = (237, 28, 36)

background_color = dark_blue

##########################################
# Formatting
pygame.font.init()
##########################################


##########################################
# CLASSES AND METHODS:
# OOP classes and their methods
##########################################

class Board:  # creates the class 'Board'
        def __init__(self):  # creates the object 'self' within the class 'Board'
                pygame.init()  # initiates all modules within the pygame library
                self.screen = pygame.display.set_mode((window_width, window_height))  # defines the instance variable self.screen as the pygame display window
                pygame.display.set_caption("Sliding Puzzle - CS 101 Final Project") # Sets the caption
                self.clock = pygame.time.Clock()  # defines an instance variable as a pygame object that can keep track of time
                self.all_sprites = pygame.sprite.Group() # Defines a list of all sprites
                self.board_size = 4 # Defines the length/width of the board as 4x4 by default
                self.unlock_6x = False # Sets both special modes to false
                self.unlcok_impossible = False
                self.unlock_impossible_perm = False

        def new(self):  # a method that will create a new board when called
                # Defines different lists as the list of tiles in their original solved form - this lists will be changed later
                self.all_sprites = pygame.sprite.Group()
                self.tiles_grid = self.create_board()
                self.starting_grid = self.create_board()
                self.winning_grid = self.create_board()
                self.white_grid = self.create_board()
                # Add the buttons:
                self.buttons_list = []
                self.buttons_list.append(Button(470 + tile_size, 50, 200, 50, "Shuffle", white, black))
                self.buttons_list.append(Button(470 + tile_size, 120, 200, 50, "Solve", white, black))
                self.buttons_list.append(Button(470 + tile_size, 190, 50, 50, "3x", white, black))
                self.buttons_list.append(Button(545 + tile_size, 190, 50, 50, "4x", white, black))
                self.buttons_list.append(Button(620 + tile_size, 190, 50, 50, "5x", white, black))
                if self.unlock_6x:
                        self.buttons_list.append(Button(470 + tile_size, 260, 200, 50, "6x6", red, black))
                if self.unlcok_impossible or self.unlock_impossible_perm: # The or statement ensures the button will still be there if the user turns impossible mode off
                        self.buttons_list.append(Button(470 + tile_size, 330, 200, 50, "Impossible", black, red)) # Add impossible button

                # Shuffle the board so it doesn't start as solved:
                self.shuffle()
                while self.check_win(): # A loop to ensure it doesnt start solved even after shuffling
                        self.shuffle()

                self.draw_tiles() # Draw the tiles to the screen

        def update(self): # Updates all tiles
                self.all_sprites.update()

        def create_board(self): # Creates default board
                grid = [[x + y * self.board_size for x in range(1, self.board_size + 1)] for y in range(self.board_size)]
                grid[-1][-1] = 0
                return grid

        def shuffle(self):  # A method that shuffles the tiles
                for a in (1, 20): # A loop that creates a list of numbers from 1 to board_size so that it can iterate over the list later
                        while True:
                                length_list = []
                                for i in range(1, self.board_size):
                                        length_list.append(i)

                                # Initialize the grid with the winning configuration
                                self.tiles_grid = self.create_board()

                                # Shuffle the tiles
                                for row in length_list:
                                        for column in length_list:
                                                rand_loc_x = random.randint(0, self.board_size - 1)
                                                rand_loc_y = random.randint(0, self.board_size - 1)
                                                if ((rand_loc_x == self.board_size - 1 and rand_loc_y) or (row and column) == self.board_size - 1):
                                                         pass
                                                else:
                                                        self.tiles_grid[row][column], self.tiles_grid[rand_loc_x][rand_loc_y] = self.tiles_grid[rand_loc_x][rand_loc_y], self.tiles_grid[row][column]

                                # Check if the shuffled board is solvable and not solved
                                if self.is_solvable(self.tiles_grid) and not self.check_win() :
                                        break



        def is_solvable(self, grid): # A method that cheks if the board can be solved
                '''A parity count is a mathematical concept that can determine if the board is solvable.
                One parity, otherwise known as an inversion, occurs when a higher-numbered tile precedes a tile
                of a lower value. If the number of parities is even, than the board is solvable. Otherwise, it is
                not solvable. See resources for more.'''

                inversion_count = 0

                # Loops through each pair of tiles
                for i in range(self.board_size * self.board_size - 1):
                        for j in range(i + 1, self.board_size * self.board_size):
                                # inversion_count is increased if it finds a pair where a larger number precedes a smaller one
                                if grid[j // self.board_size][j % self.board_size] and grid[i // self.board_size][i % self.board_size] and grid[i // self.board_size][i % self.board_size] > grid[j // self.board_size][j % self.board_size]:
                                        inversion_count += 1

                # For even grid sizes, adjust the inversion count if necessary
                if self.board_size % 2 == 0:
                        blank_row = 0
                        for i in range(self.board_size):
                                if grid[i][-1] == 0:
                                        blank_row = i
                                        break
                        if blank_row % 2 == 0:
                                inversion_count += blank_row
                        else:
                                inversion_count += self.board_size - blank_row - 1

                # The grid is solvable if inversion count is even
                return inversion_count % 2 == 0


        def draw_tiles(self): # Draws tiles to the screen
                self.tiles = [] # Creates empty list for the tiles
                for row, x in enumerate(self.tiles_grid): # Loops through each tile in self.tiles_grid
                        self.tiles.append([])
                        for column, tile in enumerate(x):
                                if tile != 0: # If the tile is not blank:
                                        if self.tiles_grid[row][column] == self.starting_grid[row][column] and not self.unlcok_impossible: # If the tile is in the same as the tile in the solved grid, make the tile green
                                                self.tiles[row].append(Tile(self, column + (origin / tile_size), row + (origin / tile_size), str(tile), green))
                                        elif self.tiles_grid[row][column] == self.starting_grid[row][column] and self.unlcok_impossible: # If the tile is in the same as the tile in the solved grid, make the tile green
                                                self.tiles[row].append(Tile(self, column + (origin / tile_size), row + (origin / tile_size), str(""), green)) # If impossible mode is turned on, don't display any text on either white or green tiles. White tiels are now black
                                        elif self.unlcok_impossible:
                                                self.tiles[row].append(Tile(self, column + (origin / tile_size), row + (origin / tile_size), str(""), black))
                                        else: # Otherwise, the tile is white
                                                self.tiles[row].append(Tile(self, column + (origin / tile_size), row + (origin / tile_size), str(tile), white))
                                else: # If the tile is blank, draw an empty tile the same color as the background
                                        self.tiles[row].append(Tile(self, column + (origin / tile_size), row + (origin / tile_size), "empty", background_color))


        def play(self):  # a method that will run the board
                self.playing = True  # defines the instance variable 'self.playing' as true
                while self.playing:  # while the board is being run
                        self.clock.tick(fps)  # start counting
                        self.events()  # Calls on various methods that are needed to play the game
                        self.update()
                        self.draw()


        def draw_grid(self): # Draws the grid that separates the tiles
                for row in range(origin, (self.board_size * tile_size) + tile_size + origin,
                                                 tile_size):  # a range from -1 to the product of self.board_size * tile_size, with an increment of tile_size
                        pygame.draw.line(self.screen, black, (row, origin), (row, (self.board_size * tile_size) + origin))
                for column in range(origin, (self.board_size * tile_size) + tile_size + origin, tile_size):
                        pygame.draw.line(self.screen, black, (origin, column), ((self.board_size * tile_size) + origin, column))

        def draw(self): # Draws all objects onto the screen
                self.screen.fill(background_color)  # fills the screen with the background color (dark blue)
                self.all_sprites.draw(self.screen) # Draws all the tiles before drawing the grid
                self.draw_grid() # Draws the grid on top of the tiles to ensure it stays on top
                for button in self.buttons_list: # Draws each button to the screen
                        button.draw(self.screen)

                if self.check_win() and self.board_size == 5: # If the user beats 5x5
                        self.unlock_6x = True # Unlock the condition for a 6x6 option
                        self.buttons_list.append(Button(470 + tile_size, 260, 200, 50, "6x6", red, black)) # Add the button temporarily until self.new adds it permanently
                        self.display_winning_message()

                if self.check_win() and self.board_size == 6: # If the user beats 6x6
                        self.unlock_impossible_perm = True # This ensures that if the user turns off impossible mode the button will still be there
                        self.unlock_impossible = True
                        self.buttons_list.append(Button(470 + tile_size, 330, 200, 50, "Impossible", black, red))
                        self.display_winning_message()

                if self.check_win(): # If the player has won, draw the winning screen on top of everything else
                        self.display_winning_message()

                pygame.display.flip()  # Updates the display

        def display_winning_message(self): # Method for displaying the win screen
                # Fill only the board area with the background color
                pygame.draw.rect(self.screen, green,(origin + 1, origin + 1, self.board_size * tile_size - 1, self.board_size * tile_size - 1))

                # Draw the winning message in the center of the board area
                font = pygame.font.SysFont("rockwell", 17 * self.board_size)
                text_surface = font.render("You Win!", True, black)
                text_rect = text_surface.get_rect(center=(origin + (self.board_size * tile_size) // 2, origin + (self.board_size * tile_size) // 2))

                self.screen.blit(text_surface, text_rect) # Sends the win screen to the game screen. From what I can tell this is similar to the flip() method but slightly different in that it's used for rect objects

        def events(self):  # a method that checks for events that are happening in the board
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:  # If the player quits the board:
                                pygame.quit()  # De-initialize all pygame modules
                                quit(0)  # Quits the program

                        if event.type == pygame.MOUSEBUTTONDOWN: # If the player clicks - I'm not sure why pygame requires all caps
                                mouse_x, mouse_y = pygame.mouse.get_pos() # Defines x and y variables for where the user clicked
                                for row, tiles in enumerate(self.tiles): # Iterates through the list of tiles in self.tiles()
                                        for column, tile in enumerate(tiles):

                                                if tile.click(mouse_x, mouse_y): # Cheks if the currently selected tie was clicked or not


                                                        '''These if statements check if the tile can go up, down, left, or right. First it checks if
                                                        the direction in question is out of bounds or not. If it isn't, in then checks if the blank
                                                        space is in that direction, and if both conditions are met, the tile and the blank space are
                                                        swapped.'''

                                                        if column + 1 < self.board_size and self.tiles_grid[row][column + 1] == 0: # Right
                                                                self.tiles_grid[row][column], self.tiles_grid[row][column + 1] = self.tiles_grid[row][column + 1], self.tiles_grid[row][column]

                                                        elif column - 1 >= 0 and column - 1 <= self.board_size and self.tiles_grid[row][column - 1] == 0: # Left
                                                                self.tiles_grid[row][column], self.tiles_grid[row][column - 1] = self.tiles_grid[row][column - 1], self.tiles_grid[row][column]

                                                        elif row + 1 < self.board_size and self.tiles_grid[row + 1][column] == 0: # Down
                                                                self.tiles_grid[row][column], self.tiles_grid[row + 1][column] = self.tiles_grid[row + 1][column], self.tiles_grid[row][column]

                                                        elif row - 1 >= 0 and row - 1 <= self.board_size and self.tiles_grid[row - 1][column] == 0: # Up
                                                                self.tiles_grid[row][column], self.tiles_grid[row - 1][column] = self.tiles_grid[row - 1][column], self.tiles_grid[row][column]
                                                        self.draw_tiles()


                                        for button in self.buttons_list:
                                                if button.click(mouse_x, mouse_y): # Passes the location that the user clicked into the method button.click to check if the button was clicked
                                                        if button.text == "Shuffle": # If the button in question says "Shuffle"
                                                                self.shuffle() # Call the shuffle method
                                                                self.draw_tiles() # Draw the tiles again

                                                        '''Note: the solve button was really only useful for testing the project before I implemented
                                                         the win screen. Right now, even though it's arranging the tiles properly, it really is just
                                                         a button for displaying the win screen.'''
                                                        if button.text == "Solve": # If the button says solve:
                                                                self.tiles_grid = self.winning_grid # Turn the grid into the solved grid
                                                                self.draw_tiles() # Update the tiles

                                                        if button.text == "3x":
                                                                self.board_size = 3 # Set the board size to 3x3

                                                                '''It seems that certain functions don't recognize the change in board size unless they're
                                                                manually called once more, so I have to call them all again here'''
                                                                self.create_board()
                                                                self.new()
                                                                self.play()
                                                                self.update()
                                                                self.draw_tiles()
                                                                self.shuffle()


                                                        if button.text == "4x":
                                                                self.board_size = 4
                                                                self.create_board()
                                                                self.new()
                                                                self.play()
                                                                self.update()
                                                                self.draw_tiles()
                                                                self.shuffle()

                                                        if button.text == "5x":
                                                                self.board_size = 5
                                                                self.create_board()
                                                                self.new()
                                                                self.play()
                                                                self.update()
                                                                self.draw_tiles()
                                                                self.shuffle()

                                                        if button.text == "6x6":
                                                                self.board_size = 6
                                                                self.create_board()
                                                                self.new()
                                                                self.play()
                                                                self.update()
                                                                self.draw_tiles()
                                                                self.shuffle()

                                                        if button.text == "Impossible": # On/Off switch for impossible mode
                                                                if self.unlcok_impossible:
                                                                        self.unlcok_impossible = False
                                                                else:
                                                                        self.unlcok_impossible = True
                                                                self.new() # Because we draw a new board it ensures the user can't 'peek' behind the blank tiles and cheat
                                                                self.play()

        def check_win(self): # If the current grid is the same as the sovled grid, return True, else return False
                if self.tiles_grid == self.starting_grid:
                        return True
                return False


class Tile(pygame.sprite.Sprite): # Class for the tiles
        def __init__(self, board, x, y, text, color): # Pass the board class, x/y position of the tile, text, and color
                self.groups = board.all_sprites # Defines instance for the group containing all sprites

                pygame.sprite.Sprite.__init__(self, self.groups) # Initializes the pygame Sprite class
                self.board = board
                self.image = pygame.Surface((tile_size, tile_size))
                self.x, self.y = x, y
                self.text = text
                self.rect = self.image.get_rect()

                if self.text != "empty": # If the tile text is not blank:
                        self.font = pygame.font.SysFont("rockwell", 50) # Set the font and size
                        font_surface = self.font.render(self.text, True, black) # Render font
                        self.image.fill(color) # Fill the tile using the color passed
                        self.font_size = self.font.size(self.text) # Set font size to what's been specified

                        draw_x = (tile_size / 2) - self.font_size[0] / 2 # Defines where the text should be drawn so it's centered
                        draw_y = (tile_size / 2) - self.font_size[1] / 2
                        self.image.blit(font_surface, (draw_x, draw_y)) # Draw the text
                else:
                        self.image.fill(background_color) # If there's no text, draw the tile the color of the background

        def update(self): # Updates location of the tile
                self.rect.x = self.x * tile_size
                self.rect.y = self.y * tile_size

        def click(self, mouse_x, mouse_y): # Checks if the passed coordinates (where the user clicked) are within the tile
                return self.rect.left <= mouse_x <= self.rect.right and self.rect.top <= mouse_y <= self.rect.bottom

class Button: # Class for the buttons on screen
        def __init__(self, x, y, width, height, text, color, text_color):
                self.color = color
                self.text_color = text_color
                self.width = width
                self.height = height
                self.x = x
                self.y = y
                self.text = text
                self.draw(board.screen)

        def draw(self, screen): # Method for drawing the buttons to the screen, essentially the same as the Tile class
                pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
                font = pygame.font.SysFont("rockwell", 30)
                text = font.render(self.text, True, self.text_color)
                self.font_size = font.size(self.text)
                draw_x = self.x + (self.width / 2) - self.font_size[0] / 2
                draw_y = self.y + (self.height / 2) - self.font_size[1] / 2
                screen.blit(text, (draw_x, draw_y))


        def click(self, mouse_x, mouse_y): # Same logic used in the Tile class
         return self.x <= mouse_x <= self.x + self.width and self.y <= mouse_y <= self.y + self.height


##########################################
# MAIN PROGRAM:
#   beginning of running program
##########################################

board = Board()
while True: # Infinite loop so the game is always playing
        board.new() # Create a new board
        board.play() # Start playing
        board.clock.tick(fps) # Tick the clock 60 times per second
