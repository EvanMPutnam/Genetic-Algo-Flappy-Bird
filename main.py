import arcade
import random
import sys
import ast

import neural

from genetic import Genetic_Algorithm

from bird import Player
from pipe import Pipe

from config import *

class Game(arcade.Window):
    # ############################################################################
    # Description:          Creates the game screen and sets everything up.
    # ############################################################################
    def __init__(self, players = 1, demo_mode = False, neural_network_to_load = neural.NeuralNetwork(4, HIDDEN_NODES, 1)):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)

        # These are the sprite lists that contain the bird/pipe objects
        self.bird_list = None
        self.pipes = None

        # Helpful genetic algorithm information.
        self.generation = 0
        self.max_score = 0
        self.global_max = 0
        self.global_reached = False
        self.player_count = players

        # This is if you are going to be testing your AI.
        self.demo_mode = demo_mode
        self.demo_network = neural_network_to_load

        # Data structures to keep track of dead birds for genetic algorithm.
        self.dead_birds_dict = {}
        self.dead_birds_array = []

        # Keeps track of which bird is doing the best in the current run.
        self.best_bird = None

    # ############################################################################
    # Description:          Sets things up for the next generation
    # ############################################################################
    def reset(self):
        self.global_reached = False
        self.generation += 1
        self.max_score = 0
        self.setup()
        self.dead_birds_array = []
        self.dead_birds_dict = {}
        
    # ############################################################################
    # Description:          Function used to configure sprites lists.  We
    #                       highjack this for setting up our sprite list with the 
    #                       genetic algorithm results.
    # ############################################################################
    def setup(self):
        self.pipes = arcade.SpriteList()
        
        # If the generation is the first we need to create the birds.

        if self.demo_mode:
            self.bird_list = arcade.SpriteList()
            self.bird_list.append(Player(neural_net = self.demo_network))
            self.player_count = 1
        else:
            if self.generation == 0:
                self.bird_list = arcade.SpriteList()
                for i in range(0, self.player_count):
                    self.bird_list.append(Player())
            # Otherwise send to the genetic algorithm to modify them.
            else:
                self.bird_list = Genetic_Algorithm.next_gen(self.dead_birds_array)


        # Create initial pipes
        left, right = Pipe.generate_pipes(SCREEN_WIDTH + 20)
        self.pipes.append(left)
        self.pipes.append(right)
        left, right = Pipe.generate_pipes(SCREEN_WIDTH + 20 + 150)
        self.pipes.append(left)
        self.pipes.append(right)
        left, right = Pipe.generate_pipes(SCREEN_WIDTH + 20 + 300)
        self.pipes.append(left)
        self.pipes.append(right)

    # ############################################################################
    # Description:          Just draw the sprites and debug text.
    # ############################################################################
    def on_draw(self):
        arcade.start_render()

        # Draw our objects to the window :) 
        self.bird_list.draw()
        self.pipes.draw()

        # Helpful neural network information printing
        arcade.draw_text("Generation: " + str(self.generation), 10, SCREEN_HEIGHT - 20, arcade.color.WHITE, 12)
        arcade.draw_text("Max Run Score: " + str(self.max_score), 10, SCREEN_HEIGHT - 40, arcade.color.WHITE, 12)
        arcade.draw_text("Max Score: " + str(self.global_max), 10, SCREEN_HEIGHT - 60, arcade.color.WHITE, 12)


    # ############################################################################
    # Description:          Update the game.  Calls into a number of other update
    #                       methods for birds and pipes.
    # ############################################################################
    def on_update(self, delta_time):

        # This is the nearest pipe, which information is sent to each birds neural network.
        nearest_pipe = None

        left, right = None, None
        pipes_to_score = 0
        for pipe in self.pipes:
            pipe.update(delta_time)
            pipe.color = self.pipes[1].color
            if not pipe.disabled and nearest_pipe == None:
                nearest_pipe = pipe
            if pipe.disabled and not pipe.scored:
                pipes_to_score += 1
                # Mark the pipe as scored.
                pipe.scored = True
            

            # If the pipe needs to be deleted then create new pices to later add.
            if pipe.delete:
                left, right = Pipe.generate_pipes(SCREEN_WIDTH + 20)

        birds_dead = 0
        bird_count = 0
        for bird in self.bird_list:
            if not bird.disabled and not bird.dead:
                bird.score += (pipes_to_score * 1000)
                collisions = arcade.check_for_collision_with_list(bird, self.pipes)
                # If the bird collides with a block then it becomes disabled.
                if len(collisions) > 0:
                    bird.disabled = True
            elif bird.dead or bird.disabled:
                birds_dead += 1
                # Add dead birds to to list to perform genetic algorithm on to modify.
                if bird_count not in self.dead_birds_dict:
                    self.dead_birds_dict[bird_count] = True
                    self.dead_birds_array.append(bird)

            # Keeps track of max score.
            if bird.score > self.max_score:
                self.max_score = bird.score
                self.best_bird = bird

            # Call the update method for our bird
            nearest_pipe.color = arcade.color.RED
            bird.update([nearest_pipe.center_y, nearest_pipe.center_x], delta_time = delta_time)
            bird_count += 1
        
        # Pop top and bottom pipes and add new ones.
        if left != None:
            self.pipes.pop(0)
            self.pipes.pop(0)
            self.pipes.append(left)
            self.pipes.append(right)

        # Determine if we need to reset the game.
        reset_needed = birds_dead == self.player_count

        # Keep track of global score across all runs and serialize the neural network.
        if self.max_score > self.global_max:
            self.global_max = self.max_score
            self.global_reached = True

        
        # If the game is about to be reset then save off the serialized data.
        if reset_needed and self.global_reached:
            data = self.best_bird.neural_net.serialize()
            # Save string of dictionary.  Can read it in with ast later.
            with open(NEURAL_NET_OUT, "w+") as fle:
                fle.write(str(data))
            print("Generation " + str(self.generation) + " of score " + str(self.global_max) + " written.")
            self.best_bird = None
            
        
        # Handle reset.
        if reset_needed:
            self.reset()
    

if __name__ == "__main__":
    window = None
    # This sets up a demo version where you can look at a single bird with a saved off neural network.
    if len(sys.argv) > 1:
        neural_network_path = sys.argv[1]
        data = ""
        with open(neural_network_path) as fle:
            data = fle.read()
        neural_net = neural.NeuralNetwork.deserialize(data)
        window = Game(demo_mode = True, neural_network_to_load = neural_net)
    # Otherwise run the genetic algorithm sim.
    else:
        window = Game(players = MAX_PLAYERS)
    window.setup()
    arcade.run()