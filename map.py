'''
CS440 Project 3
@Authors: Aditya Geria, Lawrence Maceren
@Description: 
'''

import heapq
import pygame
import random
import math
import os

from random import randint
from ast import literal_eval as make_tuple

# Initialize Screen
pygame.init()
myfont = pygame.font.SysFont("monospace", 15)

blockwidth = 6  # Drawing dimensions of block
GridCols = 100
GridRows = 100
GameScreen = pygame.display.set_mode((GridCols*blockwidth+200,GridRows*blockwidth+34))

start_x = 0
start_y = 0

cursor_x = 0
cursor_y = 0

class GridCell():
	def __init__(self,celltype):
		self.celltype = celltype
		self.count = 0
	def getType(self):
		return self.celltype
	def setType(self,newtype):
		self.celltype = newtype
	def getCount(self):
		return self.count
		
# Initialize Grid
grid = [[GridCell('N') for y in range(GridRows)] for x in range(GridCols)]

# Make Random Grid
def makeGrid(withBlocks):
	# Highways 
	needtoblock = GridCols*GridRows*0.2
	blocked = 0

	while blocked < needtoblock:
		x = randint(0,GridCols-1)
		y = randint(0,GridRows-1)
		if grid[x][y].getType()=='N':
			grid[x][y].setType('H')
			blocked += 1
	
	# Hard to Traverse
	needtoblock = GridCols*GridRows*0.2
	blocked = 0

	while blocked < needtoblock:
		x = randint(0,GridCols-1)
		y = randint(0,GridRows-1)
		if grid[x][y].getType()=='N':
			grid[x][y].setType('T')
			blocked += 1
			
	# Blocked cells
	if withBlocks == True:
		needtoblock = GridCols*GridRows*0.1
		blocked = 0

		while blocked < needtoblock:
			x = randint(0,GridCols-1)
			y = randint(0,GridRows-1)
			if grid[x][y].getType()=='N':
				grid[x][y].setType('0')
				blocked += 1

def setStart():
	# Generate Start
	x = randint(0,GridRows)
	y = randint(0,GridCols)

	while grid[x][y].getType == '0':
		x = randint(0,GridRows)
		y = randint(0,GridCols)

	start_x = x
	start_y = y
	
	return start_x,start_y

# Draw Grid
def drawGrid(myGridSurface):
	myGridSurface.fill((255,255,255))
	for x in range(len(grid)):
		for y in range(len(grid[x])):
			celltype = grid[x][y].getType()
			if celltype == '0':
				pygame.draw.rect(myGridSurface, (40,40,40), (x*blockwidth+10,y*blockwidth+10,blockwidth,blockwidth), 0)
				pygame.draw.rect(myGridSurface, (40,40,40), (x*blockwidth+10,y*blockwidth+10,blockwidth+1,blockwidth+1), 1)
			elif celltype == 'N':
				pygame.draw.rect(myGridSurface, (255,255,255), (x*blockwidth+10,y*blockwidth+10,blockwidth,blockwidth), 0)
				pygame.draw.rect(myGridSurface, (100,100,100), (x*blockwidth+10,y*blockwidth+10,blockwidth+1,blockwidth+1), 1)
			elif celltype == 'T':
				pygame.draw.rect(myGridSurface, (200,200,200), (x*blockwidth+10,y*blockwidth+10,blockwidth,blockwidth), 0)
				pygame.draw.rect(myGridSurface, (100,100,100), (x*blockwidth+10,y*blockwidth+10,blockwidth+1,blockwidth+1), 1)
			elif celltype == 'H':
				pygame.draw.rect(myGridSurface, (130,170,255), (x*blockwidth+10,y*blockwidth+10,blockwidth,blockwidth), 0)
				pygame.draw.rect(myGridSurface, (100,100,100), (x*blockwidth+10,y*blockwidth+10,blockwidth+1,blockwidth+1), 1)

	myGridSurface = myGridSurface.convert()
	return myGridSurface

# Draw Screen
def drawScreen(GridSurface):

	# Draw grid and cursor
	GameScreen.blit(GridSurface,(0,0))
	pygame.draw.rect(GameScreen, (255,0,0), (cursor_x*blockwidth+9,cursor_y*blockwidth+9,blockwidth+2,blockwidth+2), 2)

	# Draw starting point
	pygame.draw.circle(GameScreen, (255,0,0), (start_x*blockwidth+blockwidth/2+10,start_y*blockwidth+blockwidth/2+10),blockwidth/2, 0)
	
	# Draw text
	label = myfont.render("G = New Map, E = New Start, S = Save, L = Load", 1, (0,0,0))
	GameScreen.blit(label, (20, blockwidth*GridRows+14))
	
	# Draw screen
	pygame.display.update()
	
# Make and Draw Grid
GridSurface = pygame.Surface(GameScreen.get_size())
makeGrid(True)
start_x,start_y = setStart()
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
				grid = [[GridCell('N') for y in range(GridRows)] for x in range(GridCols)]
				makeGrid(True)
				GridSurface = drawGrid(GridSurface)
				start_x,start_y = setStart()
				print "Generated new map with blocks"
			elif event.key == pygame.K_e:
				start_x,start_y = setStart()
			elif event.key == pygame.K_s:
				# Save map: get filename
				filename = raw_input("Save map to: ")
				with open(os.path.join("./gen",filename),"w") as mapfile:
					mapfile.write(str((start_x,start_y)))		# Write start
					mapfile.write("\n")
					
					for y in range(len(grid[x])):				# Write each cell
						for x in range(len(grid)):
							mapfile.write(str(grid[x][y].getType()))
						mapfile.write("\n")

					mapfile.close()
				print "Map saved!"
			elif event.key == pygame.K_l:
				# Load map: get filename
				filename = raw_input("Load map from: ")
				with open(os.path.join("./gen",filename),"r") as mapfile: #changed to allow using /maps folder
					new_start = make_tuple(mapfile.readline())
					start_x = new_start[0]
					start_y = new_start[1]

					for y in range(len(grid[x])):				# Read each cell
						for x in range(len(grid)):
							grid[x][y].setType(mapfile.read(1))
						mapfile.read(1)

					mapfile.close()
				
				GridSurface = drawGrid(GridSurface)
				print "Map loaded!"
				
	# Draw Screen
	drawScreen(GridSurface)
