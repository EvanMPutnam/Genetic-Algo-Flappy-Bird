import arcade
import random
import neural
from genetic import Genetic_Algorithm
from config import *


class Player(arcade.Sprite):
    # ############################################################################
    # Description:          Only real relevant item is if we have a neural network
    #                       or not to input to the player.  Other params are
    #                       from arcade.Sprite class constructor.
    # ############################################################################
    def __init__(self, filename=DEFAULT_BIRD_TEXTURE, scale=1, image_x=0,
                 image_y=0, image_width=0, image_height=0, center_x=0,
                 center_y=0, repeat_count_x=1, repeat_count_y=1, neural_net=None):
        super().__init__(filename=filename, scale=scale, image_x=image_x, image_y=image_y,
                         image_width=image_width, image_height=image_height, center_x=center_x,
                         center_y=center_y, repeat_count_x=repeat_count_x, repeat_count_y=repeat_count_y)

        if neural_net == None:
            # Description on in_nodes:
            #   - y position of bird
            #   - y position of a piece of the nearest col
            #   - x position of nearest col
            #   - dy of bird
            self.neural_net = neural.NeuralNetwork(4, HIDDEN_NODES, 1)
            # self.neural_net.setActivationFunction(neural.tanh, neural.tanhDeriv)
        else:
            self.neural_net = neural_net

        # Initial conditions
        self.position = [BIRD_X_POSITION, random.randint(250, 450)]
        self.flap = False
        self.dead = False
        self.disabled = False
        self.dy = 0

        # Information for genetic algorithm
        self.score = 0
        self.fitness = 0

    # ############################################################################
    # Description:          Use our genetic algorithm to the bird.
    # ############################################################################
    def mutate(self):
        self.neural_net.mutate(Genetic_Algorithm.mutate(0.1))

    # ############################################################################
    # Description:          Apply gravity, determine whether to jump, etc.
    #                       This is where the neural network comes into play.
    # ############################################################################
    def update(self, nearest_pipe_data, delta_time=0):

        # See if we should flap.
        if not self.dead and not self.disabled:
            # Normalize values
            bird_y_pos = self.center_y / SCREEN_HEIGHT
            pipe_y_pos = nearest_pipe_data[0] / SCREEN_HEIGHT
            pipe_x_pos = nearest_pipe_data[1] / SCREEN_WIDTH
            bird_dy = self.dy / MAX_POSITIVE_VEL

            # Make the prediction
            input_data = [bird_y_pos, pipe_y_pos,
                          pipe_x_pos, bird_dy]
            jump_val = self.neural_net.predict(input_data)

            # If we exceed our threshold then jump!
            if jump_val[0][0] > JUMP_THRESHOLD:
                self.flap = True

            # Add some score for every moment we are not dead or disabled
            self.score += 1

        # If we are dead then don't do anything
        if self.dead:
            return
        # or if flapping/disabled apply gravity
        elif self.flap == False or self.disabled:
            self.dy += (GRAVITY * delta_time)
        # Otherwise we are flapping and apply upward value
        else:
            self.dy += (FLAPPING_VEL)
            if self.dy > MAX_POSITIVE_VEL:
                self.dy = MAX_POSITIVE_VEL
            if self.dy + self.center_y > SCREEN_HEIGHT:
                self.dy = -1

        # Reset flapping value
        self.flap = False

        # Add the change in y to the sprites center.
        self.center_y += self.dy

        # Handle death condition
        if self.center_y <= 5:
            self.dead = True
