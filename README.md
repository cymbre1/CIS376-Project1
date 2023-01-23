# Project 1, Maze Generator/Solver

Kit Bazner and Cymbre Spoehr

# Project Description
Life is incredibly complex, and sometimes impossible for us to study. For instance, it can be hard to know how a virus is spreading through a population, or how parasites travel through groups of hosts. Often, it is easier for us to make a simulation of life, and study the simulation. There are many, many types of artificial life; one of the simplest (but still pretty amazing!) is cellular automata. These take place on grids (typically), and have simple rulesets. For instance, in John Conway's classic Game of Life, cells are either alive or dead. If a cell has exactly three neighbors and is dead, it is reborn. If it has less than two neighbors and is alive, it dies from underpopulation. If it has more than three neighbors and is alive, it dies from overpopulation.


Another automata, called Mazectric, can be used for building mazes. This automata has the ruleset

* a dead cell with 3 neighbors is born
* a cell with less than 1 or more than 4 neighbors dies

# Project Specifications (copied from project description)

You may use whatever language and library you like, but you may not use an existing game engine. Do not use a JavaScript/Web based solution, as web browsers need too much control over the core loop for you to learn what we need to learn here. Some ideas are

* Python and PyGame (strongly suggested)
* Java and LWJGL (much more complicated but also more sophisticated)
* C or C++ with SDL2 (this is what PyGame uses behind the scenes). This will be the most complex, but you will also cause you to ~~want to die~~ learn the most.

Regardless of what you choose, your submission should meet the following specifications:

* Has a core game loop that is frame limited (10)
* Must have some mechanism for easily changing the framerate (be it a run time option, or a simple easy to change final variable) (10)
* Grow and draw a maze using the prescribed cellular automata method (15)
* Draw your maze at the framerate using squares for each cell (10)
Must handle quit events, mouse events, and keyboard events. Clicking the close button of the game window should gracefully shutdown the game. Clicking on a rectangle causes that rectangle to either become a new random color (if it is currently (0, 0, 0)), or become (0, 0, 0) if it has any color at all. Note that (0, 0, 0) is an open cell and can be traversed. Any other color is a wall. (15)
* Must have a circle that represents the player. The player will start at the top left corner of the maze. If there is currently a cell there, remove it before adding the player. The player must be able to move through the maze corridors, but cannot go through walls, attempting to get to the lower right corner. Making it to the lower right corner should result in a "win". Keep in mind that mouse clicks can turn on and off a wall; this is not intended to be a fun game, merely a project to get the absolute basics working before we move forward with more complicated coding (20)
* Fully commented and documented code that includes headers for all public classes and methods. If a method has a return type, or takes parameters, or throws exceptions, it should be documented. Use the Google Style Guide (https://google.github.io/styleguide/) when you have questions. (10)
You must demo your project in class on the due date for full points (10)

You. may work in a group of 1-3 people. If you choose to do the project alone, you are on the hook for making sure it all works correctly. If you work in a group, you must contribute and be able to document your contribution. You should do this by adding comments where you added code. I will take one submission per group, and only give grades to the people who have their name on the project. Adding your name to the project is your assertion that you contributed in a meaningful, fair way to the project.