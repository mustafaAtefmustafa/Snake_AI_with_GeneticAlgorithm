import numpy as np
import tkinter as tk   # For GUI.
import time as time 
import random as rand 

# Global variables.

# Directions.
UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)

MOVES = [UP, DOWN, LEFT, RIGHT]

EMPTY = 0 
FOOD = 99 

class Game:
    """Initializing game parameters."""
    def __init__(self, size, num_snakes, players, gui=None, display=False, max_turns=100):
        self.size = size
        self.num_snakes = num_snakes
        self.players = players
        self.gui = gui 
        self.display = display   # While training the agent we don't need to show the board. 
        self.max_turns = max_turns
        
        self.num_food = 4
        self.turn = 0
        self.snake_size = 3

        self.snakes = [[((j+1)*self.size//(2*self.num_snakes),
                         self.size//2+i) for i in range(self.snake_size)] for j in range(self.num_snakes)]   # Defining snakes, space each them out and centrally locate them.
       
        self.food = [(self.size//4, self.size//4), (3*self.size//4, self.size//4),
                    (self.size//4, 3*self.size//4), (3*self.size//4, 3*self.size//4)]   # Spawn food on the board.
        
        self.players_ids = [i for i in range(self.num_snakes)]   # To check who's dead and who's still alive.

        # Build the board.
        self.board = np.zeros([self.size, self.size])   # 2D array of size.
        for i in self.players_ids:
            for tup in self.snakes[i]:
                self.board[tup[0]][tup[1]] = i + 1
        for tup in self.food:
            self.board[tup[0]][tup[1]] = FOOD 

        self.food_index = 0
        self.food_xy = [(9, 4), (6, 1), (9, 9), (7, 5), (2, 6), (2, 3), (4, 3), (5, 3), (3, 7), (2, 2), (0, 7), (2, 0), (5, 4), (3, 6), (7, 1), 
(7, 3), (5, 7), (7, 1), (6, 4), (6, 0), (9, 2), (3, 6), (1, 1), (9, 1), (1, 8), (1, 2), (9, 8), (3, 8), (3, 3), (9, 8), (9, 0), (7, 8), (0, 9), (4, 0), (6, 5), (6, 6), (8, 2), (5, 5), (8, 1), (4, 3), (4, 6), (1, 6), (3, 5), (7, 6), (3, 1), (1, 8), (9, 3), (4, 8), (1, 3), (0, 1), (4, 6), (9, 0), (2, 0), (7, 6), (5, 8), (1, 1), (3, 9), (9, 1), (9, 1), (1, 1), (3, 6), (6, 1), (3, 8), (5, 9), (2, 0), (3, 6), (7, 8), (2, 4), (3, 9), (2, 9), (9, 6), (4, 9), (4, 8), (7, 3), (7, 1), (5, 
7), (8, 7), (4, 0), (0, 3), (8, 0), (5, 5), (5, 9), (6, 6), (7, 3), (9, 5), (0, 7), (7, 0), (8, 0), (7, 1), (4, 0), (8, 0), (1, 1), (3, 8), (9, 4), (4, 7), (1, 7), (2, 5), (4, 9), (9, 2), (2, 9), (5, 7), (1, 2), (7, 0), (5, 2), (5, 5), (2, 4), (3, 9), (3, 4), (7, 5), (3, 6), (2, 4), (8, 6), (4, 5), (0, 3), (6, 2), (5, 4), (8, 2), (8, 3), (3, 9), (8, 8), (2, 8), (9, 4), (2, 9), (8, 2), (0, 2), (9, 3), (3, 3), (2, 5), (2, 2), (4, 4), (8, 1), (9, 1), (9, 1), (7, 6), (4, 5), (5, 1), 
(3, 1), (0, 0), (0, 8), (7, 7), (4, 7), (7, 5), (9, 3), (6, 6), (0, 4), (9, 1), (0, 8), (7, 4), (8, 5), (3, 3), (3, 8), (0, 3), (0, 3), (7, 6), (7, 5), (7, 9), (1, 2), (7, 5), (9, 6), (2, 0), (8, 3), (7, 5), (8, 7), (2, 3), (2, 3), (4, 2), (6, 0), (6, 2), (6, 5), (5, 7), (4, 6), (1, 6), (7, 9), (8, 4), (6, 8), (6, 3), (9, 5), (2, 3), (2, 3), (9, 3), (9, 4), (2, 9), (1, 7), (4, 0), (2, 1), (5, 7), (3, 6), (3, 5), (9, 5), (0, 4), (7, 3), (8, 4), (6, 1), (2, 1), (3, 7), (3, 7), (9, 
9), (4, 2), (0, 8), (9, 5)]   # When food is eaten spawn another one in random place.
    
    def move(self):
        """Handles the logic over the board."""
        moves = []
        # Moving the head.
        for i in self.players_ids:
            snake_i = self.snakes[i]
            move_i = self.players[i].get_move(self.board, snake_i)
            moves.append(move_i)
            new_square = (snake_i[-1][0] + move_i[0], snake_i[-1][1] + move_i[1])   # The snake's head + the move.
            snake_i.append(new_square)
        
        # Updating the tail.
        for i in self.players_ids:
            head_i = self.snakes[i][-1]
            if head_i not in self.food:   # The snake didn't eat.
                self.board[self.snakes[i][0][0]][self.snakes[i][0][1]] = EMPTY   # Update the tail --> Set the last element of the snake to empty.
                self.snakes[i].pop(0)   # Remove that last element from the snake.
            else:   # The snake did eat the food.
                self.food.remove(head_i)   # Remove that food from the board.

        # Check out of the board boundaries.
        for i in self.players_ids:
            head_i = self.snakes[i][-1]
            if head_i[0] >= self.size or head_i[1] >= self.size or head_i[0] < 0 or head_i[1] < 0:
                self.players_ids.remove(i)   # Remove the player.
            else:
                self.board[head_i[0]][head_i[1]] = i + 1   # Update the board.
            
        # Check for collisions.
        for i in self.players_ids:
            head_i = self.snakes[i][-1]
            for j in range(self.num_snakes):   # Check for all snakes even the dead ones.
                if i == j:   # If we crashed into ourselves.
                    if head_i in self.snakes[i][: -1]:   # Check if the head crashes into any element of the snake except for the head itself.
                        self.players_ids.remove(i)
                else:
                    if head_i in self.snakes[j]:   # If we crash into another snake.
                        self.players_ids.remove(i)

        # Spawn new food.
        while len(self.food) < self.num_food:
            x = self.food_xy[self.food_index][0]
            y = self.food_xy[self.food_index][1]
            while self.board[x][y] != EMPTY:   # If that spot isn't empty generate new coordinates.
                self.food_index += 1
                x = self.food_xy[self.food_index][0]
                y = self.food_xy[self.food_index][1]
            self.food.append((x, y))
            self.board[x][y] = FOOD 
            self.food_index += 1
        return moves 

    def play(self, display, termination=False):
        if display:
            self.display_board()
        while True:
            if termination:
                for i in self.players_ids:
                    if len(self.snakes[0]) - self.turn/20 <= 0:   # The snake hasn't eaten for a while.
                        self.players_ids.remove(i)
                        return -2 
            if len(self.players_ids) == 0:   # There's no living players.
                return -1
            if self.turn >= self.max_turns:   # The game is broken. 
                return 0
            moves = self.move()
            self.turn += 1
            if display:
                for move in moves:
                    if move == UP:
                        print("UP")
                    elif move == RIGHT:
                        print("RIGHT")
                    elif move == LEFT:
                        print("LEFT")
                    else:
                        print("DOWN")
                self.display_board()
                if self.gui is not None:
                    self.gui.update()
                time.sleep(1)

    def display_board(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == EMPTY:
                    print("|_", end="")
                elif self.board[i][j] == FOOD:
                    print("|#", end="")
                else:
                    print("|" + str(int(self.board[i][j])), end="")
            print("|")

class Gui:
    """Intializing the GUI parameters."""
    def __init__(self, game, size):
        self.game = game
        self.size = size 
        self.game.gui = self 

        self.ratio = self.size / self.game.size
        
        #Tkinter params.
        self.app = tk.Tk()
        self.canvas = tk.Canvas(self.app, width=self.size, height=self.size)
        self.canvas.pack()

        for i in range(len(self.game.snakes)):
            color = '#' + '{0:03X}'.format((i+1)*500)
            snake = self.game.snakes[i]
            self.canvas.create_rectangle(self.ratio*(snake[-1][1]), self.ratio*(snake[-1][0]),
                                        self.ratio*(snake[-1][1]+1), self.ratio*(snake[-1][0]+1), fill=color)

            for j in range(len(snake)-1):
                color = '#' + '{0:03X}'.format((i+1)*123)
                self.canvas.create_rectangle(self.ratio*(snake[j][1]), self.ratio*(snake[j][0]),
                                            self.ratio*(snake[j][1]+1), self.ratio*(snake[j][0]+1), fill=color)

        for food in self.game.food:
            self.canvas.create_rectangle(self.ratio*(food[1]), self.ratio*(food[0]),
                                        self.ratio*(food[1]+1), self.ratio*(food[0]+1), fill='#000000000')

    def update(self):
            self.canvas.delete('all')
            for i in range(len(self.game.snakes)):
                color = '#' + '{0:03X}'.format((i+1)*500)
                snake = self.game.snakes[i]
                self.canvas.create_rectangle(self.ratio*(snake[-1][1]), self.ratio*(snake[-1][0]),
                                            self.ratio*(snake[-1][1]+1), self.ratio*(snake[-1][0]+1), fill=color)

                for j in range(len(snake)-1):
                    color = '#' + '{0:03X}'.format((i+1)*123)
                    self.canvas.create_rectangle(self.ratio*(snake[j][1]), self.ratio*(snake[j][0]),
                                                self.ratio*(snake[j][1]+1), self.ratio*(snake[j][0]+1), fill=color)

            for food in self.game.food:
                self.canvas.create_rectangle(self.ratio*(food[1]), self.ratio*(food[0]),
                                            self.ratio*(food[1]+1), self.ratio*(food[0]+1), fill='#000000000')
            self.canvas.pack()
            self.app.update()