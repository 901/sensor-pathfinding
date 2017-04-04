'''
CS440 Project 3
@Authors: Aditya Geria, Lawrence Maceren
@Description: 
'''

import heapq
import pygame
import random
import math

from random import randint
from ast import literal_eval as make_tuple

# Initialize Screen
pygame.init()
myfont = pygame.font.SysFont("monospace", 15)

blockwidth = 6  # Drawing dimensions of block
GridCols = 100
GridRows = 100
GameScreen = pygame.display.set_mode((GridCols*blockwidth+200,GridRows*blockwidth+34))

# Initialize Grid
grid = [['N' for y in range(GridRows)] for x in range(GridCols)]

cursor_x = 0
cursor_y = 0

class GridCell():
    def __init__(celltype):
        self.celltype = celltype
        self.count = 0
    def getType(self):
        return self.celltype
    def getCount(self):
        return self.count



# Make Random Grid
def makeGrid(withBlocks):
	# Highways 
	needtoblock = GridCols*GridRows*0.2
	blocked = 0

	while blocked < needtoblock:
		x = randint(0,GridCols-1)
		y = randint(0,GridRows-1)
		if grid[x][y]=='N':
			grid[x][y] = 'H'
			blocked += 1
	
	# Hard to Traverse
	needtoblock = GridCols*GridRows*0.2
	blocked = 0

	while blocked < needtoblock:
		x = randint(0,GridCols-1)
		y = randint(0,GridRows-1)
		if grid[x][y]=='N':
			grid[x][y] = 'T'
			blocked += 1
			
	# Blocked cells
	if withBlocks == True:
		needtoblock = GridCols*GridRows*0.1
		blocked = 0

		while blocked < needtoblock:
			x = randint(0,GridCols-1)
			y = randint(0,GridRows-1)
			if grid[x][y]=='N':
				grid[x][y] = '0'
				blocked += 1

# Draw Grid
def drawGrid(myGridSurface):
	myGridSurface.fill((255,255,255))
	for x in range(len(grid)):
		for y in range(len(grid[x])):
			if grid[x][y] == '0':
				pygame.draw.rect(myGridSurface, (40,40,40), (x*blockwidth+10,y*blockwidth+10,blockwidth,blockwidth), 0)
				pygame.draw.rect(myGridSurface, (40,40,40), (x*blockwidth+10,y*blockwidth+10,blockwidth+1,blockwidth+1), 1)
			elif grid[x][y] == 'N':
				pygame.draw.rect(myGridSurface, (255,255,255), (x*blockwidth+10,y*blockwidth+10,blockwidth,blockwidth), 0)
				pygame.draw.rect(myGridSurface, (100,100,100), (x*blockwidth+10,y*blockwidth+10,blockwidth+1,blockwidth+1), 1)
			elif grid[x][y] == 'T':
				pygame.draw.rect(myGridSurface, (200,200,200), (x*blockwidth+10,y*blockwidth+10,blockwidth,blockwidth), 0)
				pygame.draw.rect(myGridSurface, (100,100,100), (x*blockwidth+10,y*blockwidth+10,blockwidth+1,blockwidth+1), 1)
			elif grid[x][y] == 'H':
				pygame.draw.rect(myGridSurface, (130,170,255), (x*blockwidth+10,y*blockwidth+10,blockwidth,blockwidth), 0)
				pygame.draw.rect(myGridSurface, (100,100,100), (x*blockwidth+10,y*blockwidth+10,blockwidth+1,blockwidth+1), 1)

	myGridSurface = myGridSurface.convert()
	return myGridSurface

# Draw Screen
def drawScreen(GridSurface):

	# Draw grid and cursor
	GameScreen.blit(GridSurface,(0,0))
	pygame.draw.rect(GameScreen, (255,0,0), (cursor_x*blockwidth+9,cursor_y*blockwidth+9,blockwidth+2,blockwidth+2), 2)

	# Draw text
	label = myfont.render("G = New (w/blocks), B = New (wo/blocks)", 1, (0,0,0))
	GameScreen.blit(label, (20, blockwidth*GridRows+14))
	
	# Draw screen
	pygame.display.update()
	
# Make and Draw Grid
GridSurface = pygame.Surface(GameScreen.get_size())
makeGrid(True)
GridSurface = drawGrid(GridSurface)

# Main Loop
running = True

while(running):
	# Get Input
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				running = False
			elif event.key == pygame.K_g:
				grid = [['N' for y in range(GridRows)] for x in range(GridCols)]
				makeGrid(True)
				GridSurface = drawGrid(GridSurface)
				print "Generated new map with blocks"
			elif event.key == pygame.K_b:
				grid = [['N' for y in range(GridRows)] for x in range(GridCols)]
				makeGrid(False)
				GridSurface = drawGrid(GridSurface)
				print "Generated new map without blocks"
	
	# Draw Screen
	drawScreen(GridSurface)
