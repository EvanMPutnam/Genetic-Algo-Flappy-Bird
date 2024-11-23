from bird import Player
import random
import arcade
import numpy


class Genetic_Algorithm:

    @staticmethod
    def next_gen(birds, keep_num=10):
        Genetic_Algorithm.calculate_fitness(birds)
        total = len(birds)
        birds_list = arcade.SpriteList()

        for i in range(0, total):
            bird = Genetic_Algorithm.pick_one(birds)
            birds_list.append(bird)
        return birds_list

    @staticmethod
    def pick_one(birds):
        index = 0
        r = random.random()
        while r > 0:
            r = r - birds[index].fitness
            index += 1
        index -= 1
        bird = birds[index]
        child = Player(neural_net=bird.neural_net.copy())
        child.fitness = bird.fitness
        child.mutate()
        return child

    @staticmethod
    def calculate_fitness(birds):
        sum_v = 0
        for bird in birds:
            sum_v += bird.score

        for bird in birds:
            bird.fitness = bird.score / sum_v
            bird.score = 0

    @staticmethod
    def mutate(rate):
        # Create a function for augmentation.
        def mutate_augmented(val):
            if random.random() < rate:
                return val + float(numpy.random.normal(0, 0.1))
            else:
                return val
        return mutate_augmented
