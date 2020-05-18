Predator Prey Simulations
Created and Finalized 5/17/2020 by Jacob Hopkins
Written in python 3.7
Imports libraries:
os
pygame
datetime

uses files(found in the lib folder):
supported_input.png
grid.py
sprite.py


to run install python 3, and install pygame. then launch the predator_prey_simulation.py file.

This simulates a blindfolded person searching for prey in enviroments of differning complexities.

I currently have it setup to run completely using graphics.

The window launches to a intro screen, which can be clicked past.

The next menu lets you select the type of simulation and start it.

Then it counts down the simulation.

You start and see the prey for second, and then they disappear. You can still see the walls.

Prey are white.
Walls are black.
Predator is red.

Overlapping the predator and prey will kill a prey and keep count. 

After 60 seconds or when they are all dead, the simulation will end.

A menu will appear to allow you to save the data in the Results folder.

You can exit with the exit button, or the red X at any time.

You can play again with the play again button.

If an error somehow occurs it will exit into a crash message waiting for user input on command line.