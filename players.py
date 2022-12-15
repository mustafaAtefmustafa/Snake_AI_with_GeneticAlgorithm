from game import *
import math as math

class RandomPlayer:
    """Initializing player parameters."""

    def __init__(self, i):
        self.i = i

    def get_move(self, board, snake):
        """Get a move in a random direction."""
        r = rand.randint(0, 3)
        return MOVES[r]

class GeneticPlayer:
    """AI Agent."""
    def __init__(self, pop_size, num_generations, num_trials, window_size, hidden_size, board_size,
                mutation_chance=0.1, mutation_size=0.1):
        self.pop_size = pop_size
        self.num_generations = num_generations
        self.num_trials = num_trials   # Number of games each brain will play.
        self.window_size = window_size   # How much of the board the brain can see.
        self.hidden_size = hidden_size   # Size of the brain.
        self.board_size = board_size

        self.mutation_chance = mutation_chance   # Probability a mutation will occur when producing new generations.
        self.mutation_size = mutation_size

        ###Debug.
        self.display = False 

        # Brain selected to play games.
        self.current_brain = None
        self.pop = [self.generate_brain(self.window_size**2, self.hidden_size, len(MOVES)) for _ in range(self.pop_size)]   # Creating the population.


    def generate_brain(self, input_size, hidden_size, output_size):
        """Each brain will be a list of metrices."""
        hidden_layer1 = np.array([[rand.uniform(-1, 1) for _ in range(input_size+1)] for _ in range(hidden_size)])
        hidden_layer2 = np.array([[rand.uniform(-1, 1) for _ in range(hidden_size+1)] for _ in range(hidden_size)])
        output_layer = np.array([[rand.uniform(-1, 1) for _ in range(hidden_size+1)] for _ in range(output_size)])
        return [hidden_layer1, hidden_layer2, output_layer]

    def get_move(self, board, snake):
        """Perform forward propagation."""
        input_vector = self.process_board(board, snake[-1][0], snake[-1][1], snake[-2][0], snake[-2][1])
        hidden_layer1 = self.current_brain[0]
        hidden_layer2 = self.current_brain[1]
        output_layer = self.current_brain[2]

        # Forward propagation.
        hidden_result1 = np.array([math.tanh(np.dot(input_vector, hidden_layer1[i])) for i in range(hidden_layer1.shape[0])]+[1])   # perform a dot product with tanh activation function to make output between -1 and +1, add 1 for bias.
        hidden_result2 = np.array([math.tanh(np.dot(hidden_result1, hidden_layer2[i])) for i in range(hidden_layer2.shape[0])]+[1])
        output_result = np.array([np.dot(hidden_result2, output_layer[i]) for i in range(output_layer.shape[0])])

        max_index = np.argmax(output_result)
        return MOVES[max_index]


    def process_board(self, board, x1, y1, x2, y2):
        """Get the input positions of the snake."""
        input_vector = [[0 for _ in range(self.window_size)] for _ in range(self.window_size)]

        for i in range(self.window_size):
            for j in range(self.window_size):
                ii = x1 + i - self.window_size//2
                jj = y1 + j - self.window_size//2
                
                # If window out of bounds, snake can't move there.
                if ii < 0 or jj < 0 or ii >= self.board_size or jj >= self.board_size:
                    input_vector[i][j] = -1
                elif board[ii][jj] == FOOD:
                    input_vector[i][j] = 1
                elif board[ii][jj] == EMPTY:
                    input_vector[i][j] = 0
                else:   # It's another snake.
                    input_vector[i][j] = -1
        if self.display:
            print(np.array(input_vector))
        input_vector = list(np.array(input_vector).flatten()) + [1]   # Flatten the input vector.
        return np.array(input_vector)

    def reproduce(self, top_25):
        """Choose the best 25% of the population and create new one of them."""
        new_pop = []
        for brain in top_25:
            new_pop.append(brain)
        for brain in top_25:
            new_brain = self.mutate(brain)
            new_pop.append(new_brain)

        # Spawn new random copies of brains.
        for _ in range(self.pop_size//2):
            new_pop.append(self.generate_brain(self.window_size**2, self.hidden_size, len(MOVES)))
        return new_pop

    def mutate(self, brain):
        """Make new variations of the brain."""
        new_brain = [] 
        for layer in brain:
            new_layer = np.copy(layer)
            for i in range(new_layer.shape[0]):
                for j in range(new_layer.shape[1]):
                    if rand.uniform(0, 1) < self.mutation_chance:   # With probability of mutation chance.
                        new_layer[i][j] += rand.uniform(-1, 1) * self.mutation_size
            new_brain.append(new_layer)
        return new_brain

    def one_generation(self):
        """Each brain in the pop will play a game and then select those reproduce."""
        scores = [0 for _ in range(self.pop_size)]   # Store the scores for each brain.
        max_score = 0
        for i in range(self.pop_size):
            for j in range(self.num_trials):
                self.current_brain = self.pop[i]
                game = Game(self.board_size, 1, [self])
                outcome = game.play(False, termination=True)
                score = len(game.snakes[0])   # For single player variation.
                scores[i] += score 
                # For debugging.
                if outcome == 0:
                    print("Snake", i, "made it to the last turn")
                

                if score > max_score:
                    max_score = score
                    print(max_score, "at ID", i)

        # Testing of all the brains is complete and they are all ranked.
        top_25_indexes = list(np.argsort(scores))[3*(self.pop_size//4):self.pop_size]
        print(scores)
        top_25 = [self.pop[i] for i in top_25_indexes][::-1]   # Reverse the list to make the highest ranked brain at first.
        self.pop = self.reproduce(top_25)

    def evolve_pop(self):
        """Go through each of the generations and update the population based on how well they perform."""
        for i in range(self.num_generations):
            self.one_generation()
            print("gen", i)


        # DEBUG, display the board for each brain.
        key = input("enter any character to display boards.")
        for brain in self.pop:
            self.display = True 
            self.current_brain = brain 
            game = Game(self.board_size, 1, [self], display=True)
            gui = Gui(game, 800)
            game.play(True, termination=True)
            print("Snake length", len(game.snakes[0]))