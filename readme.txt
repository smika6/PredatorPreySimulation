Predator Prey Simulations
Created and Finalized 5/17/2020 by Jacob Hopkins
Written in python 3.7

INSTALL USE AND UNINSTALL VIDEO: https://youtu.be/Z593_uKi9Rg


INSTALL STEPS:
1. Visit: https://github.com/smika6/PredatorPreySimulation/

2. Download the Zip Folder under 'Clone or Download'

3. Open that Folder & Exctract the Contents to somewhere you know, Desktop?

4. Visit: https://www.python.org/downloads/

5. Download the install file for your system.

6. Run the installer, on windows ensure you enable adding python to 'PATH'

7. Open a Comand Prompt/Terminal

8. Type: python -m pip install -U pip
	( Refer to: https://pip.pypa.io/en/stable/installing/#upgrading-pip )

9. Type: python -m pip install -U pygame
	( Refer to: https://www.pygame.org/wiki/GettingStarted )

10. Run the file 'predator_prey_simulation.py' 

___________________________________________________________________________________________________
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



CONTROLS:

w/up arrow: move up
a/down arrow: move down
s/left arrow: move left
d/right arrow: move right
0: end the simulation abruptly
Esc: closes main simulation
Click with mouse on my boxes

file descriptions:
grid.py
	populates the grid and handles all sprites on grid
sprite.py
	handles location and movement and drawing
predator_prey_simulation.py
	handles using the grid, text, and pygame loop to run the simulation

save info:

files are saved as 
"predator_prey_simulation_" + prey distribution + "_" + enviroment complexity + "_data" (+ buffer) + ".txt"

what does that mean?
it will save it like this:
	"predator_prey_simulation_random_moderate_data.txt"

and if that file already exists then it will save:
	"predator_prey_simulation_random_moderate_data_1.txt"

and just simply count higher until it saves a new file, to not delete old data.
and it will save into the Results folder.
here is sample save data:

Simulation taken on 05/17/20 at 16:20:10 PM
Simulation Prey Distribution: random
Simulation Enviroment Complexity: moderate
Simulation Time Durration: 60
Simulation Total Prey in Simulation: 50
Simulation Total Prey Left Alive: 50
Simulation Total Prey Killed: 0

that way the student can open each to get data, and see at a glance if they do or dont have some simulation trial yet just by file name.
