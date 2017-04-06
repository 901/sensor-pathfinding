'''
CS440 Project 3
@Authors: Aditya Geria, Lawrence Maceren
@Description:
'''

import heapq
import time
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

agentx = 0
agenty = 0

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
				grid[x][y].setType('B')
				blocked += 1

def setStart():
	# Generate Start
	x = randint(0,GridRows-1)
	y = randint(0,GridCols-1)

	while grid[x][y].getType == 'B':
		x = randint(0,GridRows-1)
		y = randint(0,GridCols-1)

	agentx = x
	agenty = y

	return agentx,agenty

# Draw Grid
def drawGrid(myGridSurface):
	myGridSurface.fill((255,255,255))
	for x in range(len(grid)):
		for y in range(len(grid[x])):
			celltype = grid[x][y].getType()
			if celltype == 'B':
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
	pygame.draw.circle(GameScreen, (255,0,0), (agentx*blockwidth+blockwidth/2+10,agenty*blockwidth+blockwidth/2+10),blockwidth/2, 0)

	# Draw text
	label = myfont.render("G = New Map, E = New Start, S = Save, L = Load", 1, (0,0,0))
	GameScreen.blit(label, (20, blockwidth*GridRows+14))

	# Draw screen
	pygame.display.update()

#1 = up
#2 = down
#3 = left
#4 = right
def makeActions():
	s = ""
	dir = ['U', 'L', 'D', 'R']
	for x in range(0,100):
		rand = random.randint(0, 3)
		s += str(dir[rand])
	return s

def ground_truth_data1(s):
	global agentx, agenty
	print len(s)
	print "agent x is " + str(agentx) + " agent y is " + str(agenty)
	rand = 0
	sensor = ""
	celltype = ""
	with open("ground_truth.txt", "w") as f:
		# Write start
		f.write("(" + str(agentx) + "," + str(agenty) + ")\n")
		
		# Iterate
		for c in s:
			print c,
			#time.sleep(0.5)
			if c == 'U':
				rand = random.randint(1,100)
				#move according to 90/10 probability
				if rand <= 90:
					try:
						if agenty-1 >= 0 and grid[agentx][agenty-1].getType() != 'B':		# Check for block or out of bounds
							agenty -= 1
							#f.write(str(agentx) + "," + str(agenty))
							print "agent x is " + str(agentx) + " agent y is " + str(agenty)
						#else:
							#f.write(str(agentx) + "," + str(agenty))
							#agentx = agentx
					except IndexError:
						agentx = agentx
				#else:
					#f.write(str(agentx) + "," + str(agenty))
				celltype = grid[agentx][agenty].getType()
				rand = random.randint(1,100)
				if rand <= 90:
					sensor += celltype
				elif rand > 90 and rand <= 95:
					if celltype == 'N':
						sensor += 'H'
					elif celltype == 'T':
						sensor += 'N'
					else:
						sensor += 'T'
				else:
					if celltype == 'N':
						sensor += 'T'
					elif celltype == 'T':
						sensor += 'H'
					else:
						sensor += "N"
			elif c == 'D':
				rand = random.randint(1,100)
				#move according to 90/10 probability
				if rand <= 90:
					try:
						if agenty+1 < GridRows and grid[agentx][agenty+1].getType() != 'B':		# Check for block or out of bounds:
							agenty += 1
							#f.write(str(agentx) + "," + str(agenty))
							print "agent x is " + str(agentx) + " agent y is " + str(agenty)
						#else:
							#f.write(str(agentx) + "," + str(agenty))
							#agentx = agentx
					except IndexError:
						agentx = agentx
				#else:
					#f.write(str(agentx) + "," + str(agenty))
				celltype = grid[agentx][agenty].getType()
				rand = random.randint(1,100)
				if rand <= 90:
					sensor += celltype
				elif rand > 90 and rand <= 95:
					if celltype == 'N':
						sensor += 'H'
					elif celltype == 'T':
						sensor += 'N'
					else:
						sensor += 'T'
				else:
					if celltype == 'N':
						sensor += 'T'
					elif celltype == 'T':
						sensor += 'H'
					else:
						sensor += "N"
			elif c == 'L':
				rand = random.randint(1,100)
				#move according to 90/10 probability
				if rand <= 90:
					try:
						if agentx-1 >= 0 and grid[agentx-1][agenty].getType() != 'B':		# Check for block or out of bounds:
							agentx -= 1
							#f.write(str(agentx) + "," + str(agenty))
							print "agent x is " + str(agentx) + " agent y is " + str(agenty)
						#else:
							#f.write(str(agentx) + "," + str(agenty))
					except IndexError:
							agentx = agentx
				#else:
					#f.write(str(agentx) + "," + str(agenty))
				celltype = grid[agentx][agenty].getType()
				rand = random.randint(1,100)
				if rand <= 90:
					sensor += celltype
				elif rand > 90 and rand <= 95:
					if celltype == 'N':
						sensor += 'H'
					elif celltype == 'T':
						sensor += 'N'
					else:
						sensor += 'T'
				else:
					if celltype == 'N':
						sensor += 'T'
					elif celltype == 'T':
						sensor += 'H'
					else:
						sensor += "N"
			elif c == 'R':
				rand = random.randint(1,100)
				#move according to 90/10 probability
				if rand <= 90:
					try:
						if agentx+1 < GridCols and grid[agentx+1][agenty].getType() != 'B':		# Check for block or out of bounds
							agentx += 1
							#f.write(str(agentx) + "," + str(agenty))
							print "agent x is " + str(agentx) + " agent y is " + str(agenty)
						#else:
							#f.write(str(agentx) + "," + str(agenty))
					except IndexError:
						agentx = agentx
				#else:
					#f.write(str(agentx) + "," + str(agenty))
				celltype = grid[agentx][agenty].getType()
				rand = random.randint(1,100)
				if rand <= 90:
					sensor += celltype
				elif rand > 90 and rand <= 95:
					if celltype == 'N':
						sensor += 'H'
					elif celltype == 'T':
						sensor += 'N'
					else:
						sensor += 'T'
				else:
					if celltype == 'N':
						sensor += 'T'
					elif celltype == 'T':
						sensor += 'H'
					else:
						sensor += "N"
			else:
				print "Came across unknown value, exiting"
				exit(0)
			f.write("(" + str(agentx) + "," + str(agenty) + ")\n")
			drawScreen(GridSurface)
			#f.write("\n")

		f.write("Transition data:\n")
		for c in s:
			f.write(c+"\n")
		f.write("Sensor data:\n")
		for c in sensor:
			f.write(c+"\n")
	drawScreen(GridSurface)
	print "agent x is " + str(agentx) + " agent y is " + str(agenty)
	print sensor
	print len(sensor)
	return agentx, agenty



# Make and Draw Grid
GridSurface = pygame.Surface(GameScreen.get_size())
makeGrid(True)
agentx,agenty = setStart()
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
				agentx,agenty = setStart()
				print "Generated new map with blocks"
			elif event.key == pygame.K_e:
				agentx,agenty = setStart()
			elif event.key == pygame.K_UP:
				if cursor_y-1 >= 0:
					cursor_y -= 1
			elif event.key == pygame.K_LEFT:
				if cursor_x-1 >= 0:
					cursor_x -= 1
			elif event.key == pygame.K_RIGHT:
				if cursor_x+1 < GridCols:
					cursor_x += 1
			elif event.key == pygame.K_DOWN:
				if cursor_y+1 < GridRows:
					cursor_y += 1
			elif event.key == pygame.K_s:
				# Save map: get filename
				filename = raw_input("Save map to: ")
				with open(os.path.join("./gen",filename),"w") as mapfile:
					mapfile.write(str((agentx,agenty)))		# Write start
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
					agentx = new_start[0]
					agenty = new_start[1]

					for y in range(len(grid[x])):				# Read each cell
						for x in range(len(grid)):
							grid[x][y].setType(mapfile.read(1))
						mapfile.read(1)

					mapfile.close()

				GridSurface = drawGrid(GridSurface)
				print "Map loaded!"
			elif event.key == pygame.K_c:
				s = makeActions()
				print "agent x is " + str(agentx) + " agent y is " + str(agenty)
				agentx, agenty = ground_truth_data1(s)
				GridSurface = drawGrid(GridSurface)
			elif event.key == pygame.K_v:		# load ground truth file
				# Load map: get filename
				filename = raw_input("Load truth file from: ")
				#with open(os.path.join("./gen",filename),"r") as mapfile: #changed to allow using /maps folder
				with open(filename,"r") as mapfile: #changed to allow using /maps folder
					new_start = make_tuple(mapfile.readline())
					agentx = new_start[0]
					agenty = new_start[1]

					for y in range(len(grid[x])):				# Read each cell
						for x in range(len(grid)):
							grid[x][y].setType(mapfile.read(1))
						mapfile.read(1)

					mapfile.close()

	# Draw Screen
	drawScreen(GridSurface)
