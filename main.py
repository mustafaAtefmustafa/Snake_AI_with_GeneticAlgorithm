from game import *
from players import *

size = 10
num_snakes = 1
players = [RandomPlayer(0)]

gui_size = 500


#game = Game(size, num_snakes, players, gui=None, display=True, max_turns=100)
#gui = Gui(game, gui_size)
#game.play(True, termination=False)


pop_size = 10
num_generations = 6000
num_trials = 1
window_size = 7
hidden_size = 15
board_size = 10
gen_player = GeneticPlayer(pop_size, num_generations, num_trials, window_size, hidden_size, board_size,
                           mutation_chance=0.1, mutation_size=0.1)
gen_player.evolve_pop()