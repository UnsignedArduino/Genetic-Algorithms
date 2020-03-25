# Genetic-Algorithms
A bunch of genetic algorithms written in Python 3.

[```Genetic Algorithm```](https://github.com/UnsignedArduino/Genetic-Algorithms/tree/master/Genetic%20Algorithms) is a Windows 10 virtual enviroment made in PyCharm. So this means that you will have to select/use a different interpeter if you are on Mac OSX or a Linux/UNIX based OS.
# Path Finding
Run [```path_finding.py```](https://github.com/UnsignedArduino/Genetic-Algorithms/blob/master/Genetic%20Algorithms/path_finding.py)
## Settings
Edit this in [```path_finding.py```](https://github.com/UnsignedArduino/Genetic-Algorithms/blob/master/Genetic%20Algorithms/path_finding.py). It is a class.
```
class Constants(object):
    # Width of play room. Also width of screen, be careful with values!
    WIDTH = 400
    # Height of play room. Also height of screen, be careful with values!
    HEIGHT = 300
    # Color to use as start
    START_COLOR = (255, 0, 0)
    # Color to use as barrier
    BARRIER_COLOR = (255, 255, 0)
    # Color to use as end
    END_COLOR = (0, 255, 0)
    # Color of sprite
    SPRITE_COLOR = (0, 0, 255)
    # Color when sprite touched end
    TOUCHED_COLOR = (0, 0, 0)
    # Sprite size
    SPRITE_SIZE = (16, 16)
    # Length of sprite, should match above
    SPRITE_LENGTH = 16
    # FPS
    SPEED = 50
    # How many generations to go through
    GENERATIONS = 100
    # Number of creatures per generation
    POPULATION = 100
    # Length of list of instructions to do
    DNA_LENGTH = 250
    # Chance out of 1 to change an instruction
    MUTATION_RATE = 0.01
```
