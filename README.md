# Genetic Algorithm Flappy Bird:
Using a neural network created from another project (See [here](https://github.com/EvanMPutnam/Python-Neural-Network)) along with the general genetic algorithm code from coding train (see [here](https://github.com/CodingTrain/website/tree/master/CodingChallenges/CC_100.5_NeuroEvolution_FlappyBird/P5)), this application will train a neural network AI to play Flappy Bird.

![Image](assets\multiple_player.PNG)

## Pre-Reqs:
* Numpy
* PyArcade

## Assets:
The art assets are from a repository here from user sourabhv. 


## Saving configuration:
During the main program the best global neural network will be serialized and saved to a file name neural.

## Loading a Configuration:
If you want to run your AI on a single bird then you just have to pass in the name of the data file that was saved off from a run.  Here is an example.
```
python main.py neural_example
```

![Image](assets\single_player.PNG)

Note that the pipe in red is the pipe whose information is currently being sent to the neural network.  We only need one pipes information because the spacing between pipes is consistent for every item.  Its just redundant data at that point.
