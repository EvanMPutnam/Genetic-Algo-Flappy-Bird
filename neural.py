import math
import copy
import json
import random

from matrix import Matrix

# ################################################
# Description:      An object that stores function
#                   pointers to an activation 
#                   function and its deriviative 
#                   function.
# ################################################
class ActivationFunction:
    def __init__(self, func, dFunc):
        self.func = func
        self.dFunc = dFunc


# ################################################
# Description:      The following four functions 
#                   are activation functions.
# ################################################

def sigmoid(e):
    return 1 / (1 + math.exp(-e))

def sigmoidDeriv(e):
    return e * (1 - e)

def tanh(e):
    return math.tanh(e)

def tanhDeriv(e):
    return 1 - (e * e)


# ################################################
# Description:      The magic neural network class
#
# Inputs:           in_nodes: input nodes for matrix.
#                   hidden_nodes: nodes in hidden layer.
#                   out_nodes: nodes expected in output.
#
# Functions:        setLearningRate: Does what it says.
#
#                   copy: Deepcopys the neural network.
#
#                   setActivationFunction: Can assign 
#                     new activation functions.
#
#                   train: Give input array and output to train on.
#
#                   predict: Give an input array to predict.
#
#                   mutate: Mutates based on function given.
#
#                   serialize: Creates a string representation of object.
#
#                   class.deserialize: Takes a string representation and 
#                       creates a new obj
#
#
# Additional Docs:  https://github.com/CodingTrain/Toy-Neural-Network-JS/blob/master/lib/nn.js
#                   You can view the library that this was ported from at the above link.
# ################################################
class NeuralNetwork:
    def __init__(self, in_nodes, hidden_nodes, out_nodes):
        # Assign numbers to node layer count.
        self.input_nodes = in_nodes
        self.hidden_nodes = hidden_nodes
        self.output_nodes= out_nodes

        # Create the needed variables.
        self.weights_ih = Matrix(self.hidden_nodes, self.input_nodes)
        self.weights_ho = Matrix(self.output_nodes, self.hidden_nodes)
        self.weights_ih.randomize()
        self.weights_ho.randomize()

        self.bias_h = Matrix(self.hidden_nodes, 1)
        self.bias_o = Matrix(self.output_nodes, 1)
        self.bias_h.randomize()
        self.bias_o.randomize()

        # Set defaults
        self.setLearningRate()
        self.setActivationFunction()

    def copy(self):
        return copy.deepcopy(self)

    def setLearningRate(self, learning_rate = 0.1):
        self.learning_rate = learning_rate

    def setActivationFunction(self, func = sigmoid, dFunc = sigmoidDeriv):
        self.activation_function = ActivationFunction(func, dFunc)
    
    def predict(self, input_array):
        inputs = Matrix.fromArray(input_array)
        
        hidden = Matrix.multiply(self.weights_ih, inputs) \
                .add(self.bias_h) \
                .map(self.activation_function.func)
    
        output = Matrix.multiply(self.weights_ho, hidden) \
                .add(self.bias_o) \
                .map(self.activation_function.func)

        return output.toArray()

    def train(self, input_array, target_array):
        inputs = Matrix.fromArray(input_array)

        hidden = Matrix.multiply(self.weights_ih, inputs) \
                    .add(self.bias_h) \
                    .map(self.activation_function.func)


        outputs = Matrix.multiply(self.weights_ho, hidden) \
                    .add(self.bias_o) \
                    .map(self.activation_function.func)

        targets = Matrix.fromArray(target_array)

        output_errors = Matrix.subtractMatrices(targets, outputs)

        gradients = Matrix.map(outputs, self.activation_function.dFunc) \
                        .multiplySelf(output_errors) \
                        .multiplySelf(self.learning_rate)


        hidden_T = Matrix.transposeMatrix(hidden)
        weight_ho_deltas = Matrix.multiply(gradients, hidden_T)

        self.weights_ho = self.weights_ho.add(weight_ho_deltas)
        self.bias_o = self.bias_o.add(gradients)

        who_t = Matrix.transposeMatrix(self.weights_ho)
        hidden_errors = Matrix.multiply(who_t, output_errors)

        hidden_gradient = Matrix.map(hidden, self.activation_function.dFunc) \
                            .multiplySelf(hidden_errors) \
                            .multiplySelf(self.learning_rate)

        inputs_T = Matrix.transposeMatrix(inputs)
        weight_ih_deltas = Matrix.multiply(hidden_gradient, inputs_T)

        self.weights_ih = self.weights_ih.add(weight_ih_deltas)
        self.bias_h = self.bias_h.add(hidden_gradient)

    def serialize(self):
        pass

    def mutate(self, func):
        self.weights_ih = self.weights_ih.map(func)
        self.weights_ho = self.weights_ho.map(func)
        self.bias_h = self.bias_h.map(func)
        self.bias_o = self.bias_o.map(func)

    def serialize(self):
        data = {
            "input_nodes": self.input_nodes, 
            "output_nodes": self.output_nodes, 
            "hidden_nodes": self.hidden_nodes, 
            "weights_ih": self.weights_ih.serialize(),
            "weights_ho": self.weights_ho.serialize(),
            "bias_h": self.bias_h.serialize(),
            "bias_o": self.bias_o.serialize(),
            "learning_rate": self.learning_rate,
            "activation_function_name": self.activation_function.func.__name__,
        }
        return json.dumps(data)

    @staticmethod
    def deserialize(data):
        loaded = json.loads(data)
        nn = NeuralNetwork(loaded['input_nodes'], 
                            loaded['hidden_nodes'], 
                            loaded['output_nodes'])
        nn.weights_ih = Matrix.deserialize(loaded['weights_ih'])
        nn.weights_ho = Matrix.deserialize(loaded['weights_ho'])
        nn.bias_h = Matrix.deserialize(loaded['bias_h'])
        nn.bias_o = Matrix.deserialize(loaded['bias_o'])
        nn.learning_rate = loaded['learning_rate']
        func = loaded['activation_function_name']
        if "sigmoid" in func:
            nn.activation_function = ActivationFunction(sigmoid, sigmoidDeriv)
        else:
            nn.activation_function = ActivationFunction(tanh, tanhDeriv)
        return nn

