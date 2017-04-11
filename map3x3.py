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

blockwidth = 60  # Drawing dimensions of block
GridCols = 3
GridRows = 3
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
	heatmap = [[0 for y in range(GridRows)] for x in range(GridCols)]
	
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

# Initialize heat map
def initHeatMap():
	return [[[0.5 for y in range(GridRows)] for x in range(GridCols)] for t in range(101)]

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
			elif celltype == 'N': #or celltype == 'T' or celltype == 'H':
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

# Draw Heatmap
'''def drawHeatmap(HeatSurface,GridSurface,heatmap,time):
	HeatSurface.blit(GridSurface,(0,0))
	for x in range(len(grid)):
		for y in range(len(grid[x])):
			#print str(heatmap[x][y]*255)
			pygame.draw.rect(HeatSurface, (heatmap[x][y]*255,0,0), (x*blockwidth+10,y*blockwidth+10,blockwidth,blockwidth), 0)

	#label = myfont.render(str(time), 1, (0,0,0))
	#HeatSurface.blit(label, (10+blockwidth*GridCols+20, 160))
	HeatSurface = HeatSurface.convert()
	return HeatSurface'''
	
def drawHeatmap(HeatSurface,GridSurface,heatmap,time):
	HeatSurface = GridSurface.copy()
	RectSurface = pygame.Surface((blockwidth,blockwidth))
	RectSurface.fill((255,0,0))
	RectSurface.set_alpha(128)
	for x in range(len(grid)):
		for y in range(len(grid[x])):
			if grid[x][y].getType() != 'B':
				#myalpha = 100*heatmap[x][y]+50
				#RectSurface.set_alpha(myalpha)
				
				RectSurface.fill((heatmap[x][y]*255,0,255*(1-heatmap[x][y])))
				
				HeatSurface.blit(RectSurface,(x*blockwidth+10,y*blockwidth+10))

	#label = myfont.render(str(time), 1, (0,0,0))
	#HeatSurface.blit(label, (10+blockwidth*GridCols+20, 160))
	HeatSurface = HeatSurface.convert()
	return HeatSurface
	
# Draw Screen
def drawScreen(GridSurface,HeatSurface,heat_toggle,t,location,transitions,sensing,start_x,start_y,goal_x,goal_y):

	# Draw grid and cursor
	GameScreen.blit(GridSurface,(0,0))
	#pygame.draw.rect(GameScreen, (255,0,0), (cursor_x*blockwidth+9,cursor_y*blockwidth+9,blockwidth+2,blockwidth+2), 2)
	
	'''print "Sleeping"
	time.sleep(2)
	print "Done sleeping"'''
	
	# Draw heatmap
	#HeatSurface.set_alpha(128)
	if heat_toggle == True:
		GameScreen.blit(HeatSurface,(0,0))
	
	'''print "Sleeping"
	time.sleep(2)
	print "Done sleeping"'''
	
	# Draw start and end point
	#pygame.draw.circle(GameScreen, (255,0,0), (start_x*blockwidth+blockwidth/2+10,start_y*blockwidth+blockwidth/2+10),blockwidth/2, 0)
	#pygame.draw.circle(GameScreen, (0,255,0), (goal_x*blockwidth+blockwidth/2+10,goal_y*blockwidth+blockwidth/2+10),blockwidth/2, 0)
	
	# Draw current agent location
	if location != []:
		pygame.draw.circle(GameScreen, (0,255,0), (location[t][0]*blockwidth+blockwidth/2+10,location[t][1]*blockwidth+blockwidth/2+10),int(blockwidth*.4), 0)
	
	# Draw text
	label = myfont.render("G = New Map, E = New Start, S = Save, L = Load", 1, (0,0,0))
	GameScreen.blit(label, (20, blockwidth*GridRows+14))
	
	# Draw time
	label = myfont.render("t = "+str(t), 1, (0,0,0))
	GameScreen.blit(label, (10+blockwidth*GridCols+20, 30))

	# Draw transition
	if transitions != []:
		label = myfont.render("Action: "+str(transitions[t]), 1, (0,0,0))
		GameScreen.blit(label, (10+blockwidth*GridCols+20, 50))
	
	# Draw sensing
	if sensing != []:
		label = myfont.render("Sense: "+str(sensing[t]), 1, (0,0,0))
		GameScreen.blit(label, (10+blockwidth*GridCols+20, 70))
	
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
			#drawScreen(GridSurface)
			#f.write("\n")

		f.write("Transition data:\n")
		for c in s:
			f.write(c+"\n")
		f.write("Sensor data:\n")
		for c in sensor:
			f.write(c+"\n")
	#drawScreen(GridSurface)
	print "FINAL: agent x is " + str(agentx) + " agent y is " + str(agenty)
	print sensor
	print len(sensor)
	return agentx, agenty

# Forward Algorithm (Question D)
def forwardAlgorithm(transition,sensing):
	heatmap = initHeatMap()
	
	# t = 0 is the initial heatmap, where every cell has an equal probability
	# heatmap[t=1] is after the first action and first sensing
	
	t = 1
	
	while t <= 100:
		# Inherit old beliefs
		#heatmap[t] = heatmap[t-1]
		heatmap[t] = [[heatmap[t-1][x][y] for y in range(GridRows)] for x in range(GridCols)]
		
		#print str(t) + ": [" + str(len(heatmap[t])) + "][" + str(len(heatmap[t][0])) + "]"
		
		# Iterate grid
		for y in range(GridRows):
			for x in range(GridCols):
				#print str(t) + ": " + str(x) + ", " + str(y)
				# Get action and new state coordinates
				new_x = x
				new_y = y
				
				if transition[t] == 'L':
					new_x = x-1
				elif transition[t] == 'R':
					new_x = x+1
				elif transition[t] == 'U':
					new_y = y-1
				elif transition[t] == 'D':
					new_y = y+1
				
				oldprob = heatmap[t-1][x][y]
				oldprob_not = 1 - oldprob
				
				# Calculate observation model
				celltype = grid[x][y].getType()
				
				if celltype == sensing[t]:
					obs = 0.9
				else:
					obs = 0.1
				
				# Calculate transition model
				# Probability of ending in state s' given action a in state s
				if new_x < 0 or new_y < 0 or new_x >= GridCols or new_y >= GridRows:		# Out of bounds
					newprob = 0
				elif grid[new_x][new_y].getType() == 'B': # Hitting wall
					newprob = 0
				elif grid[x][y].getType() == 'B':		# On a wall
					heatmap[t][x][y] = 0
					continue
				else:	# Normal cell
					#If neighboring cell
					newprob = 0.1
					heatmap[t][new_x][new_y] = 0.9 * heatmap[t-1][x][y]
				
				# Apply prior belief
				newprob_old = new_prob
				newprob_not = 1 - newprob
				
				newprob = newprob_old * oldprob + newprob_not * oldprob_not
				newprob_not = newprob_not * oldprob + newprob_old * oldprob_not
				
				# Multiply by observation model
				newprob = obs * newprob
				newprob_not = (1 - obs) * newprob_not
				
				#print "Old: <" + str(oldprob) + "," + str(oldprob_not) + "> ... New: <" + str(newprob/(newprob+ newprob_not)) + "," + str(newprob_not/(newprob + newprob_not)) + ">"
				heatmap[t][newx][newy] = newprob/(newprob + newprob_not)
				
		t += 1
	return heatmap

# Error Calculation for Filtering (Question E)
def error_filtering(heatmap,location):
	print "Check error for filtering"
	
	with open("error_filtering.txt", "w") as f:
		
		# Take readings, ignore first 5
		t = 6
		while t <= 100:
			# Find probability of cell where agent is actually located
			true_x = location[t][0]
			true_y = location[t][1]
			
			prob_true_location = heatmap[t][true_x][true_y]
			
			# Find cell with max probability
			max_prob = 0
			max_x = 0
			max_y = 0
			for y in range(GridRows):
				for x in range(GridCols):
					if heatmap[t][x][y] > max_prob:
						max_x = x
						max_y = y
						max_prob = heatmap[t][x][y]
				
			# Calculate distance (euclidean)
			distance = math.sqrt((true_x - max_x)**2+(true_y - max_y)**2)
			
			# Write to file (t, distance, probability) 
			f.write(str(t) + "," + str(distance) + "," + str(prob_true_location) + "\n")
			t += 1
		
		f.close()
	
	print "Wrote error to file"

# Make and Draw Grid
GridSurface = pygame.Surface(GameScreen.get_size())
makeGrid(True)
agentx,agenty = setStart()
GridSurface = drawGrid(GridSurface)

heatmap = initHeatMap()
HeatSurface = pygame.Surface(GameScreen.get_size())
HeatSurface = drawHeatmap(HeatSurface,GridSurface,heatmap[1],1)

heatmap_toggle = False

# Initialize truth data
location_truth = []
transition_truth = []
sensing_truth = []

start_x = -1
start_y = -1
goal_x = -1
goal_y = -1

# Main Loop
running = True

test_time = 1

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
				
				location_truth = []
				transition_truth = []
				sensing_truth = []
				
				HeatSurface = drawHeatmap(HeatSurface,GridSurface,heatmap[1],1)
				
				print "Generated new map with blocks"
			elif event.key == pygame.K_e:
				agentx,agenty = setStart()
			#elif event.key == pygame.K_UP:
			#	if cursor_y-1 >= 0:
			#		cursor_y -= 1
			elif event.key == pygame.K_LEFT:
				if test_time-1 > 0:
					test_time -= 1
					HeatSurface = drawHeatmap(HeatSurface,GridSurface,heatmap[test_time],test_time)
			#elif event.key == pygame.K_RIGHT:
			#	if cursor_x+1 < GridCols:
			#		cursor_x += 1
			elif event.key == pygame.K_RIGHT:
				if test_time+1 <= 100:
					test_time += 1
					HeatSurface = drawHeatmap(HeatSurface,GridSurface,heatmap[test_time],test_time)
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
				
				location_truth = []
				transition_truth = []
				sensing_truth = []
				
				heatmap = initHeatMap()
				HeatSurface = drawHeatmap(HeatSurface,GridSurface,heatmap[test_time],test_time)
				
				GridSurface = drawGrid(GridSurface)
				print "Map loaded!"
			elif event.key == pygame.K_c:
				s = makeActions()
				print "agent x is " + str(agentx) + " agent y is " + str(agenty)
				agentx, agenty = ground_truth_data1(s)
				GridSurface = drawGrid(GridSurface)
				print "Made new ground_truth.txt"
			elif event.key == pygame.K_t:		# load ground truth file
				location_truth = []
				transition_truth = []
				sensing_truth = []
				heatmap = initHeatMap()
				HeatSurface = drawHeatmap(HeatSurface,GridSurface,heatmap[test_time],test_time)
				
				# Load map: get filename
				#filename = raw_input("Load truth file from: ")
				filename = "ground_truth.txt"
				#with open(os.path.join("./gen",filename),"r") as mapfile: #changed to allow using /maps folder
				with open(filename,"r") as truthfile: #changed to allow using /maps folder
					new_start = make_tuple(truthfile.readline())
					start_x = new_start[0]
					start_y = new_start[1]
					
					location_truth.append(new_start)
					# Get true location data
					for y in range(0,100):
						location_truth.append(make_tuple(truthfile.readline()))
					
					truthfile.readline()			# Skip title of section
					
					goal_x = location_truth[99][0]
					goal_y = location_truth[99][1]
					
					transition_truth.append("NA")
					# Get true transition data
					for y in range(0,100):				# Get true location data
						transition_truth.append(truthfile.read(1))
						truthfile.read(1)
					
					truthfile.readline()			# Skip title of section
					
					sensing_truth.append("NA")
					# Get true sensing data
					for y in range(0,100):				# Get true location data
						sensing_truth.append(truthfile.read(1))
						truthfile.read(1)
					
					truthfile.close()
					print "Truth file loaded"
			elif event.key == pygame.K_h:		# run truth file/generate heat map
				#heatmap = initHeatMap()
				#print str(transition_truth)
				heatmap = forwardAlgorithm(transition_truth,sensing_truth)
				
				test_time = 1
				HeatSurface = drawHeatmap(HeatSurface,GridSurface,heatmap[test_time],test_time)
				print "Heat maps generated"
			elif event.key == pygame.K_q:		# get error calculation for filtering (Question E)
				myerror = error_filtering(heatmap,location_truth)
			elif event.key == pygame.K_z:		# drawing toggle for heatmap
				if heatmap_toggle == False:
					heatmap_toggle = True
				else:
					heatmap_toggle = False

	# Draw Screen
	drawScreen(GridSurface,HeatSurface,heatmap_toggle,test_time,location_truth,transition_truth,sensing_truth,start_x,start_y,goal_x,goal_y)
