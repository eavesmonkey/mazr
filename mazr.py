#! /usr/bin/env python3
# Creates random mazes, using a Recursive Backtracking algorithm. Output printed in a txt file.
# Currently supports only square mazes. Smallest maze size width is 5.

import logging
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
logging.disable(logging.DEBUG)

import random, os

width='11'
height='11'
counter = 0
holeSymbol = '-' # '-' 'e'
wallSymbol = 'w' # '0' 'w'

# ask user for input
while True:
    width = input('Maze width ')
    height = width

    if width.isdecimal() and height.isdecimal():
        if int(width) < 5:
            print('Minimum allowed width is 5!')
        elif int(width) > 5 and int(width) % 2 == 0:
            print('Width must be an uneven number. Increased width size with 1.')
            height = width = int(width) + 1
            break
        else:
            break
    else:
        print('Height and width must be non floating numbers!')

# Directions
N,E,S,W = [-2, 0], [0, 2], [2, 0], [0, -2]
startpoint = [0,0]
visitedGrid = []

while True:
    startpointX = random.randint(0,int(width))
    startpointY = random.randint(0,int(height))
    if (startpointX % 2 == 1 and startpointY % 2 == 1 and
    startpointX != 0 and startpointX != int(width) and
    startpointY != 0 and startpointY != int(height)):
        startpoint = [startpointX,startpointY]
        break

logging.debug('Maze starts at: ' + str(startpoint))

def formatAndSave(maze):
    for k in range(len(maze)):
        maze[k] = ','.join(maze[k])

    maze = '\n'.join(maze)
    #logging.debug(maze)
    if not os.path.exists('mazes'):
        os.makedirs('mazes')
        
    mazeFile = open('mazes/generatedMaze.txt', 'w')
    mazeFile.write(str(maze))
    return print('Maze formatted and saved.')

def generateMaze(width, height):
    mazeList = []

    #build outer frame
    for i in range(0, int(width)):
        column = []

        for j in range(0, int(height)):
            # first row, last row, first column, last column are always walls
            if i == int(width) - 1 or i % 2 == 0:
                column.append(wallSymbol)
            else:
                if j % 2 == 0:
                    column.append(wallSymbol)
                else:
                    column.append(holeSymbol)
        mazeList.append(column)
    return mazeList

def cutHole(direction):
    global maze

    # bypass the walls
    shift = [0,0]
    if direction[0] < 0:
        shift[0] = 1
    elif direction[0] == 0:
        shift[0] = 0
    else:
        shift[0] = -1

    if direction[1] < 0:
        shift[1] = 1
    elif direction[1] == 0:
        shift[1] = 0
    else:
        shift[1] = -1

    #cut hole
    hole = [startpoint[0] + shift[0], startpoint[1] + shift[1]]
    maze[hole[0]][hole[1]] = holeSymbol
    logging.debug("Punched a hole at: " + str(hole))

def createPath(start):
    global startpoint
    global counter
    directionList = [N,S,E,W]

    while True:
        if len(directionList) != 0:
            direction = random.choice(directionList)
            logging.debug("Chosen direction: " + str(direction))
            x, y = direction[0] + start[0], direction[1] + start[1]
        else:
            # No suitable direction found, go back 1 step in the visited visitedGrid
            counter += 1
            startpoint = visitedGrid[counter * -1]
            break


        # keep looking for a valid direction
        if x > 0 and x < int(width) - 1 and y > 0 and y < int(width) - 1 and [x,y] not in visitedGrid:
            startpoint = [x, y]
            counter = 0
            visitedGrid.append(startpoint)
            logging.debug("Moving to: " + str(direction))
            cutHole(direction)
            break
        else:
            logging.debug('directions list: ' + str(directionList))
            # Choose different direction
            directionList.remove(direction)



    logging.debug("New start point set at: " + str(startpoint))

maze = generateMaze(width, height)

while True:
    createPath(startpoint)
    logging.debug("visitedGrid length " + str(len(visitedGrid)))
    if len(visitedGrid) == ((int(width) - 1) / 2) * ((int(height) - 1) / 2):
        break

#Save and format created maze
formatAndSave(maze)
