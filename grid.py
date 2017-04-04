'''
CS440 Project 1 Phase 1 - Pathfinding
@Authors: Aditya Geria, Lawrence Maceren
@Description: This project provides a way to compare the optimality and speed of different pathfinding algorithms
We compare A*, Weighted A* and Uniform-Cost under 5 different Heuristics in a maze generated
using Pygame.
In the maze, there will be different types of terrains, and the aim of Phase 1 will be to see
which heuristics and search algorithms provide the best results in terms of optimality and efficiencyr

Project 1 Phase 2 - Sequential and Integrated heuristics with A*
@Description: In Phase 2, we implement sequential heuristics using (n) priority queues, each with different
heuristic functions. With this, we can select the best possible expansion in a round robin fashion until
values from the queue are no longer admissible to the condition. We also implement Integrated heuristics which
uses two queues instead of (n) queues.
'''


import heapq
import pygame
import random
import os
import math
import time
from random import randint
from ast import literal_eval as make_tuple

# Initialize Screen
pygame.init()
myfont = pygame.font.SysFont("monospace", 15)

blockwidth = 6  # Drawing dimensions of block
GridCols = 160
GridRows = 120
GameScreen = pygame.display.set_mode((GridCols*blockwidth+200,GridRows*blockwidth+34))

# Initialize Grid
grid = [['1' for y in range(GridRows)] for x in range(GridCols)]
start_x = 0
start_y = 0
goal_x = 1
goal_y = 1

cursor_x = 0
cursor_y = 0

# Make Random Grid
def makeGrid():
	# Make 8 hard to traverse areas
	areasmade = 0
	areacoordinates = []
	while areasmade < 8:
		area_x = randint(0,GridCols-1)
		area_y = randint(0,GridRows-1)

		if (area_x,area_y) not in areacoordinates:
			areacoordinates.append((area_x,area_y))
			for x in range(area_x-15,area_x+15):
				if x >= 0 and x < GridCols:
					for y in range(area_y-15,area_y+15):
						if y >= 0 and y < GridRows:
							# 20% chance of this being hard to traverse
							if randint(0,9) < 5:
								grid[x][y] = '2'

			#drawScreen()
			areasmade += 1


	# Make 4 rivers
	riversmade = 0

	while riversmade < 4:
		makeriver = True
		rivercells = []

		# Select a starting boundary
		x = randint(1,GridCols-2)
		y = randint(1,GridRows-2)

		startside = randint(0,3)	# 0 = North, 1 = East, 2 = South, 3 = West
		if startside == 0:
			y = 0
			direction = 2
			#direction = random.choice([1,2,3])
		elif startside == 1:
			x = GridCols-1
			direction = 3
			#direction = random.choice([0,2,3])
		elif startside == 2:
			y = GridRows-1
			direction = 0
			#direction = random.choice([0,1,3])
		else:
			x = 0
			direction = 1
			#direction = random.choice([0,1,2])

		travelled = 0
		totaltravelled = 0

		while True:
			# Quit if out of bounds
			if x<0 or x>=GridCols or y<0 or y>=GridRows:
				break

			# Quit if crossed a river, do not make river
			if grid[x][y] == 'a' or grid[x][y] == 'b':
				makeriver = False
				break
			if (x,y) in rivercells:
				makeriver = False
				break

			rivercells.append((x,y))
			travelled += 1
			totaltravelled += 1

			# Move to next cell
			if direction == 0:
				y -= 1
			elif direction == 1:
				x += 1
			elif direction == 2:
				y += 1
			else:
				x -= 1

			# Change directions if travelled 20 cells
			if travelled >= 20:
				travelled = 0
				if randint(0,9) > 6:		# 40% chance change directions
					if direction == 0:
						direction = random.choice([1,3])
					elif direction == 1:
						direction = random.choice([0,2])
					elif direction == 2:
						direction = random.choice([1,3])
					else:
						direction = random.choice([0,2])

		if totaltravelled < 100:
			makeriver = False

		if makeriver == True:
			for cell in rivercells:
				if grid[cell[0]][cell[1]] == '1':
					grid[cell[0]][cell[1]] = 'a'
				else:
					grid[cell[0]][cell[1]] = 'b'

			riversmade += 1

	# Blocked cells
	needtoblock = GridCols*GridRows*0.2
	blocked = 0

	while blocked < needtoblock:
		x = randint(0,GridCols-1)
		y = randint(0,GridRows-1)
		if grid[x][y]=='1' or grid[x][y]=='2':
			grid[x][y] = '0'
			blocked += 1

	# Return the coordinates of hard to traverse areas
	return areacoordinates

# Generate Start and Finish
def generateStartFinish():
	# Generate Start
	x = randint(0,39)
	y = randint(0,39)
	if x>20:
		x = GridCols-x+20
	if y>20:
		y = GridRows-y+20

	while grid[x][y]=='a' or grid[x][y]=='b' or grid[x][y]=='0':
		x = randint(0,39)
		y = randint(0,39)
		if x>20:
			x = GridCols-x+20
		if y>20:
			y = GridRows-y+20

	start_x = x
	start_y = y

	# Generate Finish
	while grid[x][y]=='a' or grid[x][y]=='b' or grid[x][y]=='0' or math.sqrt((x-start_x)**2+(y-start_y)**2)<100:
		x = randint(0,39)
		y = randint(0,39)
		if x>20:
			x = GridCols-x+20
		if y>20:
			y = GridRows-y+20

	goal_x = x
	goal_y = y

	return start_x,start_y,goal_x,goal_y

# Draw Grid
def drawGrid(myGridSurface):
	myGridSurface.fill((255,255,255))
	for x in range(len(grid)):
		for y in range(len(grid[x])):
			if grid[x][y] == '0':
				pygame.draw.rect(myGridSurface, (40,40,40), (x*blockwidth+10,y*blockwidth+10,blockwidth,blockwidth), 0)
				pygame.draw.rect(myGridSurface, (40,40,40), (x*blockwidth+10,y*blockwidth+10,blockwidth+1,blockwidth+1), 1)
			elif grid[x][y] == '1':
				pygame.draw.rect(myGridSurface, (255,255,255), (x*blockwidth+10,y*blockwidth+10,blockwidth,blockwidth), 0)
				pygame.draw.rect(myGridSurface, (100,100,100), (x*blockwidth+10,y*blockwidth+10,blockwidth+1,blockwidth+1), 1)
			elif grid[x][y] == '2':
				pygame.draw.rect(myGridSurface, (200,200,200), (x*blockwidth+10,y*blockwidth+10,blockwidth,blockwidth), 0)
				pygame.draw.rect(myGridSurface, (100,100,100), (x*blockwidth+10,y*blockwidth+10,blockwidth+1,blockwidth+1), 1)
			elif grid[x][y] == 'a':
				pygame.draw.rect(myGridSurface, (130,170,255), (x*blockwidth+10,y*blockwidth+10,blockwidth,blockwidth), 0)
				pygame.draw.rect(myGridSurface, (100,100,100), (x*blockwidth+10,y*blockwidth+10,blockwidth+1,blockwidth+1), 1)
			elif grid[x][y] == 'b':
				pygame.draw.rect(myGridSurface, (70,90,220), (x*blockwidth+10,y*blockwidth+10,blockwidth,blockwidth), 0)
				pygame.draw.rect(myGridSurface, (100,100,100), (x*blockwidth+10,y*blockwidth+10,blockwidth+1,blockwidth+1), 1)

	myGridSurface = myGridSurface.convert()
	return myGridSurface

# Draw Screen
def drawScreen(GridSurface,closed_list,path,pathcost,nodes_expanded,mode,elapsedtime,fn_g,fn_f,fn_h):

	GameScreen.blit(GridSurface,(0,0))

	pygame.draw.circle(GameScreen, (255,0,0), (start_x*blockwidth+blockwidth/2+10,start_y*blockwidth+blockwidth/2+10),blockwidth/2, 0)
	pygame.draw.circle(GameScreen, (0,0,255), (goal_x*blockwidth+blockwidth/2+10,goal_y*blockwidth+blockwidth/2+10),blockwidth/2, 0)

	pygame.draw.rect(GameScreen, (255,0,0), (cursor_x*blockwidth+9,cursor_y*blockwidth+9,blockwidth+2,blockwidth+2), 2)

	# Draw text
	label = myfont.render("G = New Grid | E = New Endpoints | U = Uniform Cost | A = A* Search | W = Weighted A* | V = Visited | S = Save | L = Load", 1, (0,0,0))
	GameScreen.blit(label, (20, blockwidth*GridRows+14))

	label = myfont.render("Cell: ("+str(cursor_x)+","+str(cursor_y)+")", 1, (0,0,0))
	GameScreen.blit(label, (10+blockwidth*GridCols+30, 30))

	label = myfont.render("Type: "+grid[cursor_x][cursor_y], 1, (0,0,0))
	GameScreen.blit(label, (10+blockwidth*GridCols+30, 50))


	label = myfont.render("Start: ("+str(start_x)+","+str(start_y)+")", 1, (0,0,0))
	GameScreen.blit(label, (10+blockwidth*GridCols+30, 80))
	label = myfont.render("Goal: ("+str(goal_x)+","+str(goal_y)+")", 1, (0,0,0))
	GameScreen.blit(label, (10+blockwidth*GridCols+30, 100))

	if pathcost != 0:
		label = myfont.render("Path Cost:", 1, (0,0,0))
		GameScreen.blit(label, (10+blockwidth*GridCols+30, 130))
		label = myfont.render(str(pathcost), 1, (0,0,0))
		GameScreen.blit(label, (10+blockwidth*GridCols+30, 150))

	if pathcost != 0:
		label = myfont.render("Nodes Expanded:", 1, (0,0,0))
		GameScreen.blit(label, (10+blockwidth*GridCols+30, 170))
		label = myfont.render(str(nodes_expanded), 1, (0,0,0))
		GameScreen.blit(label, (10+blockwidth*GridCols+30, 190))

	if (cursor_x,cursor_y) in fn_f:
		label = myfont.render("f: "+str(fn_f[(cursor_x,cursor_y)]), 1, (0,0,0))
		GameScreen.blit(label, (10+blockwidth*GridCols+30, 220))

	if (cursor_x,cursor_y) in fn_g:
		label = myfont.render("g: "+str(fn_g[(cursor_x,cursor_y)]), 1, (0,0,0))
		GameScreen.blit(label, (10+blockwidth*GridCols+30, 240))

	if (cursor_x,cursor_y) in fn_h:
		label = myfont.render("h: "+str(fn_h[(cursor_x,cursor_y)]), 1, (0,0,0))
		GameScreen.blit(label, (10+blockwidth*GridCols+30, 260))

	label = myfont.render("Time: ", 1, (0,0,0))
	GameScreen.blit(label, (10+blockwidth*GridCols+30, 290))
	label = myfont.render(str(elapsedtime*1000)+" ms", 1, (0,0,0))
	GameScreen.blit(label, (10+blockwidth*GridCols+30, 310))

	label = myfont.render("Neighbors:", 1, (0,0,0))
	GameScreen.blit(label, (10+blockwidth*GridCols+30, 340))

	draw_y = 360
	neighbors = getNeighbors(cursor_x,cursor_y)

	for neighbor in neighbors:
		label = myfont.render("("+str(neighbor[0])+","+str(neighbor[1])+")", 1, (0,0,0))
		GameScreen.blit(label, (10+blockwidth*GridCols+30, draw_y))
		draw_y += 20

	# Draw Final Path and Closed List
	if mode == 1:
		for cell in closed_list:
			pygame.draw.circle(GameScreen, (0,255,0), (cell[0]*blockwidth+blockwidth/2+10,cell[1]*blockwidth+blockwidth/2+10),blockwidth/4, 0)
	for cell in path:
		pygame.draw.circle(GameScreen, (255,0,0), (cell[0]*blockwidth+blockwidth/2+10,cell[1]*blockwidth+blockwidth/2+10),blockwidth/4, 0)

	pygame.display.update()

# Get neighbors of a cell
def getNeighbors(x,y):
	myneighbors = [(x-1,y-1),(x,y-1),(x+1,y-1),(x-1,y),(x+1,y),(x-1,y+1),(x,y+1),(x+1,y+1)]
	myneighbors[:] = [neighbor for neighbor in myneighbors if neighbor[0]>=0 and neighbor[1]>=0 and neighbor[0]<GridCols and neighbor[1]<GridRows and grid[neighbor[0]][neighbor[1]] != '0']

	return myneighbors

def cost(currx, curry, nextx, nexty):
	cost = 0.0

	if (grid[currx][curry] == 'a' or grid[currx][curry] == '1') and (grid[nextx][nexty] == 'a' or grid[nextx][nexty] == '1'):
		if((currx == nextx - 1 or currx == nextx + 1) and (curry == nexty - 1 or curry == nexty + 1)):
			#traversing unblocked diagonally
			cost = math.sqrt(2)
		else:
			#traversing unblocked diagonally
			cost = 1
	if (grid[currx][curry] == 'b' or grid[currx][curry] == '2') and (grid[nextx][nexty] == '2' or grid[nextx][nexty] == 'b'):
		if((currx == nextx - 1 or currx == nextx + 1) and (curry == nexty - 1 or curry == nexty + 1)):
			#traversing unblocked diagonally
			cost = math.sqrt(8)
		else:
			#traversing unblocked diagonally
			cost = 2
	if (grid[currx][curry] == 'a' or grid[currx][curry] == '1') and (grid[nextx][nexty] == '2' or grid[nextx][nexty] == 'b'):
		if((currx == nextx - 1 or currx == nextx + 1) and (curry == nexty - 1 or curry == nexty + 1)):
			#traversing unblocked diagonally
			cost = (math.sqrt(2) + math.sqrt(8)) / 2
		else:
			#traversing unblocked diagonally
			cost = 1.5
	if (grid[currx][curry] == '2' or grid[currx][curry] == 'b') and (grid[nextx][nexty] == '1' or grid[nextx][nexty] == 'a'):
		if((currx == nextx - 1 or currx == nextx + 1) and (curry == nexty - 1 or curry == nexty + 1)):
			#traversing unblocked diagonally
			cost = (math.sqrt(2) + math.sqrt(8)) / 2
		else:
			#traversing unblocked diagonally
			cost = 1.5
	if (grid[currx][curry] == 'a' or grid[currx][curry] == 'b') and (grid[nextx][nexty] == 'a' or grid[nextx][nexty] == 'b') and (((currx == nextx + 1 or currx == nexty - 1) and curry == nexty) or ((curry == nexty + 1 or curry == nexty - 1) and currx == nextx)):
		cost = cost / 4
		return cost
	if cost == 0.0:
		print "Could not find cost value. Current: " + str(currx) + ", " + str(curry) + " of type: " + grid[currx][curry] + "/Next: " + str(nextx) + ", " + str(nexty) + " of type: " + grid[nextx][nexty]


	return cost

# A* Stuff

class Coordinate:
	def __init__(self, x, y, parent):
		self.x = x
		self.y = y
		self.parent = parent

	def get_x(self):
		return self.x

	def get_y(self):
		return self.y

	def get_parent(self):
		return self.parent

class PriorityQueue:
	def __init__(self):
		self.elements = []

	def empty(self):
		return len(self.elements) == 0

	def put(self, priority, item):
		heapq.heappush(self.elements, (priority, item))

	def get(self):
		return heapq.heappop(self.elements)[1]

	def getPriority(self):
		return heapq.heappop(self.elements)[0]

	def getFull(self):
		if self.empty() == False:
			return heapq.heappop(self.elements)
		return -1

	def remove(self, item):
		if item in self.elements:
			self.elements.remove(item)
			heapq.heapify(self.elements)
			return 0
		return -1

#(priority, item)
#put(priority, item)
class AStarSearch(object):
	def Search(self, startx, starty, goalx, goaly, choice):
		fringe = PriorityQueue()
		start = Coordinate(startx, starty, None)
		goal = (goalx, goaly)
		fringe.put(0, start)

		closed_list = {}
		cost_added = {}
		final_path = []
		heuristic_list = {}
		priority_list = {}
		closed_list[(start.get_x(),start.get_y())] = None
		cost_added[(start.get_x(),start.get_y())] = 0

		# f = priority_list[]
		# g = cost_added[]
		# h = heuristic

		while not fringe.empty():
			current = fringe.get()
			#print "got current from fringe with x %d and y %d" % current[0], current[1]
			if (current.get_x(),current.get_y()) == goal:
				print "Made it to goal at " + str(goal[0]) + "," + str(goal[1])

				# Make a straight path from goal to start
				PathNode = current

				while PathNode != None:
					final_path.append((PathNode.get_x(),PathNode.get_y()))
					#print "Path: " + str(current.get_x()) + "," + str(current.get_y())
					PathNode = PathNode.get_parent()

				break

			for next in getNeighbors(current.get_x(), current.get_y()):
				#print "current x %d current y %d" % current[0], current[1]
				new_cost = cost_added[(current.get_x(),current.get_y())] + cost(current.get_x(), current.get_y(), next[0], next[1])

				if next not in cost_added or new_cost < cost_added[next]:
				#if next not in closed_list or new_cost < cost_added[next]:
					cost_added[next] = new_cost		# g
					myheuristic = self.heuristic(next[0], next[1], goal_x, goal_y, choice)
					priority = new_cost + myheuristic
					heuristic_list[next] = myheuristic
					priority_list[next] = priority
					fringe.put(priority, Coordinate(next[0],next[1],current))
					closed_list[next] = current

		return closed_list, cost_added, final_path, cost_added[(goalx,goaly)], priority_list, heuristic_list

	def heuristic(self,startx,starty,goalx,goaly,choice):
		start = (startx, starty)
		goal = (goalx, goaly)
		choice = int(choice)

		if choice == 2: #manhattan
				heuristic = abs(int(startx) - int(goalx)) + abs(int(starty) - int(goaly))
				heuristic *= (1.0 + (0.25/160)) #tie-breaker by multiplying the heuristic by (minimum cost)/(max possible path length)
				return heuristic
		if choice == 1: #euclidean
				heuristic = math.sqrt(((int(startx) - int(goalx)) ** 2) + ((int(starty) - int(goaly)) ** 2))
				heuristic *= (1.0 + (0.25/160)) #tie-breaker by multiplying the heuristic by (minimum cost)/(max possible path length)
				return heuristic
		if choice == 3: #octile
				dx = abs(int(startx) - int(goalx))
				dy = abs(int(starty) - int(goaly))
				heuristic = (dx + dy) + (math.sqrt(2) - 2) * min(dx, dy)
				heuristic *= (1.0 + (0.25/160)) #tie-breaker by multiplying the heuristic by (minimum cost)/(max possible path length)
				return heuristic
		if choice == 4: #Chebyshev
				heuristic = max(abs(startx - goalx), abs(starty - goaly))
				heuristic *= (1.0 + (0.25/160))
				return heuristic
		if choice == 5: #5th heuristic
				heuristic = math.sqrt(2)*min(abs(startx - goalx), abs(starty - goaly)) + max(abs(startx - goalx), abs(starty - goaly)) - min(abs(startx - goalx), abs(starty - goaly))
				heuristic *= (1.0 + (0.25/160))
				return heuristic
		if choice == 6: #Best - minimum of all
				dx = abs(int(startx) - int(goalx))
				dy = abs(int(starty) - int(goaly))
				h1 = dx + dy
				h2 = math.sqrt(((int(startx) - int(goalx)) ** 2) + ((int(starty) - int(goaly)) ** 2))
				h3 = (dx + dy) + (math.sqrt(2) - 2) * min(dx, dy)
				h4 = max(dx, dy)
				h5 = math.sqrt(2)*min(dx, dy) + max(dx, dy) - min(dx, dy)
				h6 = min(h1, h2, h3, h4, h5)
				h6 *= (1.0 + (0.25/160))
				return h6
		return 0

class UniformCostSearch(AStarSearch):
	def Search(self,startx, starty, goalx, goaly):
		return super(UniformCostSearch, self).Search(startx,starty,goalx,goaly,1)
	def heuristic(self,startx, starty, goalx, goaly, choice):
		return 1

class WeightedAStarSearch(AStarSearch):
	def __init__(self,weight):
		self.weight = weight
	def heuristic(self,startx, starty, goalx, goaly, choice):
		return super(WeightedAStarSearch, self).heuristic(startx,starty,goalx,goaly,choice) * float(self.weight)


#Phase 2 Begin
#put(priority, item)
class SequentialAStarSearch(AStarSearch):
	def Search(self,startx, starty, goalx, goaly):
		fringe = [PriorityQueue() for x in range(5)]
		start = Coordinate(startx, starty, None)
		goal = (goalx, goaly)

		closed_list = [dict() for y in range (0,5)]
		cost_added = [dict() for y in range (0,5)]
		heuristic_list = [dict() for y in range(0,5)]
		final_path = []
		priority_list = [dict() for y in range(0,5)]
		w2 = 1.15 #weight
		path_cost = 0

		for i in range(0, 5):
			closed_list[i] = {}
			cost_added[i] = {}
			heuristic_list[i] = {}
			for next in getNeighbors(start.get_x(), start.get_y()):
				#print "current x %d current y %d" % current[0], current[1]
				new_cost = cost(start.get_x(), start.get_y(), next[0], next[1])
				if next not in cost_added[i] or new_cost < cost_added[i][next]:
					#if next not in closed_list or new_cost < cost_added[next]:
					cost_added[i][next] = new_cost		# g
					myheuristic = self.heuristic(next[0], next[1], goal_x, goal_y, i+1)
					priority = new_cost + myheuristic
					heuristic_list[i][next] = myheuristic
					priority_list[i][next] = priority
					fringe[i].put(priority, Coordinate(next[0],next[1],start))
					closed_list[i][next] = start
			closed_list[i][(start.get_x(), start.get_y())] = None
			cost_added[i][(start.get_x(), start.get_y())] = 0
			cost_added[i][(goalx, goaly)] = float("inf")
		# f = priority_list[]
		# g = cost_added[]
		# h = heuristic
		anchor = fringe[0].getFull()
		while not fringe[0].empty():
			for i in range(1, 5):
				#anchor is a tuple (priority, item)

				temp = fringe[i].getFull() #temp is a tuple (item, priority)

				#[0] = priority
				#[1] = item

				if temp != -1 and temp[0] <= w2*anchor[0]: #main condition
					#print "Not using anchor"
					if temp[1].get_x() == goalx and temp[1].get_y() == goaly:
							# Found goal, return path
							print "Made it to goal at " + str(goal[0]) + "," + str(goal[1])
							path_cost = 0
							# Make a straight path from goal to start
							PathNode = temp[1]
							old_x = PathNode.get_x()
							old_y = PathNode.get_y()
							final_path.append((old_x,old_y))
							PathNode = PathNode.get_parent()

							while PathNode != None:
								path_cost += cost(PathNode.get_x(),PathNode.get_y(),old_x,old_y)
								final_path.append((PathNode.get_x(),PathNode.get_y()))
								#print "Path: " + str(current.get_x()) + "," + str(current.get_y())
								old_x = PathNode.get_x()
								old_y = PathNode.get_y()
								PathNode = PathNode.get_parent()

							#break
							return closed_list, cost_added, final_path, path_cost, priority_list, heuristic_list
					else:
						#print "adding to fringe[" + str(i)+"]"
						for next in getNeighbors(temp[1].get_x(), temp[1].get_y()):
							#print "current x %d current y %d" % current[0], current[1]
							new_cost = cost_added[i][(temp[1].get_x(),temp[1].get_y())] + cost(temp[1].get_x(), temp[1].get_y(), next[0], next[1])

							if next not in cost_added[i] or new_cost < cost_added[i][next]:
								#print "Added neighbor to queues"
								#if next not in closed_list or new_cost < cost_added[next]:
								cost_added[i][next] = new_cost		# g
								myheuristic = self.heuristic(next[0], next[1], goalx, goaly, i+1)
								priority = new_cost + myheuristic
								heuristic_list[i][next] = myheuristic
								priority_list[i][next] = priority
								fringe[i].put(priority, Coordinate(next[0],next[1],temp[1]))
								closed_list[i][next] = temp[1]

				else:
					#print "------------- Reached the else condition, using fringe[0] ---------------"
					if anchor[1].get_x() == goalx and anchor[1].get_y() == goaly:
							# Found goal, return path
							print "Made it to goal at " + str(goal[0]) + "," + str(goal[1])
							path_cost = 0
							# Make a straight path from goal to start
							PathNode = anchor[1]
							old_x = PathNode.get_x()
							old_y = PathNode.get_y()
							final_path.append((old_x,old_y))
							PathNode = PathNode.get_parent()

							while PathNode != None:
								path_cost += cost(PathNode.get_x(),PathNode.get_y(),old_x,old_y)
								final_path.append((PathNode.get_x(),PathNode.get_y()))
								#print "Path: " + str(current.get_x()) + "," + str(current.get_y())
								old_x = PathNode.get_x()
								old_y = PathNode.get_y()
								PathNode = PathNode.get_parent()
							#break
							return closed_list, cost_added, final_path, path_cost, priority_list, heuristic_list
					else:
						#print "-------------- adding to fringe[0] ---------------"
						for next in getNeighbors(anchor[1].get_x(), anchor[1].get_y()):
							#print "current x %d current y %d" % current[0], current[1]
							new_cost=cost_added[0][(anchor[1].get_x(), anchor[1].get_y())]+cost(anchor[1].get_x(),anchor[1].get_y(),next[0],next[1])

							if next not in cost_added[0] or new_cost < cost_added[0][next]:
								#print "Added neighbor to anchor"
							#if next not in closed_list or new_cost < cost_added[next]:
								cost_added[0][next] = new_cost		# g
								myheuristic = self.heuristic(next[0], next[1], goalx, goaly, 1)
								priority = new_cost + myheuristic
								heuristic_list[0][next] = myheuristic
								priority_list[0][next] = priority
								fringe[0].put(priority, Coordinate(next[0],next[1],anchor[1]))
								closed_list[0][next] = anchor[1]
					anchor = fringe[0].getFull()


		return closed_list, cost_added, final_path, path_cost, priority_list, heuristic_list

class IntegratedAStarSearch(AStarSearch):
	def Search(self,startx, starty, goalx, goaly):
		fringe = [PriorityQueue() for x in range(5)]
		start = Coordinate(startx, starty, None)
		goal = (goalx, goaly)

		closed_list = {}
		closed_list_anchor = {}
		cost_added = {}
		heuristic_list = [dict() for y in range(0,5)]
		final_path = []
		priority_list = [dict() for y in range(0,5)]
		w2 = 1.15 # weight
		path_cost = 0

		for i in range(0, 5):
			heuristic_list[i] = {}
			for next in getNeighbors(start.get_x(), start.get_y()):
				#print "current x %d current y %d" % current[0], current[1]
				new_cost = cost(start.get_x(), start.get_y(), next[0], next[1])
				if next not in cost_added or new_cost < cost_added[next]:
					#if next not in closed_list or new_cost < cost_added[next]:
					cost_added[next] = new_cost		# g
					myheuristic = self.heuristic(next[0], next[1], goal_x, goal_y, i+1)
					priority = new_cost + myheuristic
					heuristic_list[i][next] = myheuristic
					priority_list[i][next] = priority
					fringe[i].put(priority, Coordinate(next[0],next[1],start))
					closed_list[next] = start

		closed_list[(start.get_x(), start.get_y())] = None
		closed_list_anchor[(start.get_x(), start.get_y())] = None

		cost_added[(start.get_x(), start.get_y())] = 0
		cost_added[(goalx, goaly)] = float("inf")

		# f = priority_list[]
		# g = cost_added[]
		# h = heuristic
		anchor = fringe[0].getFull()

		while not fringe[0].empty():
			for i in range(1, 5):
				#anchor is a tuple (priority, item)

				temp = fringe[i].getFull() #temp is a tuple (item, priority)

				#[0] = priority
				#[1] = item

				if temp != -1 and temp[0] <= w2*anchor[0]: #main condition
					#print "Not using anchor"
					if temp[1].get_x() == goalx and temp[1].get_y() == goaly:
							# Found goal, return path
							print "Made it to goal at " + str(goal[0]) + "," + str(goal[1])
							path_cost = 0
							# Make a straight path from goal to start
							PathNode = temp[1]
							old_x = PathNode.get_x()
							old_y = PathNode.get_y()
							final_path.append((old_x,old_y))
							PathNode = PathNode.get_parent()

							while PathNode != None:
								path_cost += cost(PathNode.get_x(),PathNode.get_y(),old_x,old_y)
								final_path.append((PathNode.get_x(),PathNode.get_y()))
								#print "Path: " + str(current.get_x()) + "," + str(current.get_y())
								old_x = PathNode.get_x()
								old_y = PathNode.get_y()
								PathNode = PathNode.get_parent()

							#break
							return [closed_list,closed_list_anchor], cost_added, final_path, path_cost, priority_list, heuristic_list
					else:
						#print "adding to fringe[" + str(i)+"]"
						for j in range(1,5):
							fringe[j].remove(temp[1])

						# Expand
						for next in getNeighbors(temp[1].get_x(), temp[1].get_y()):
							#print "current x %d current y %d" % current[0], current[1]
							new_cost = cost_added[(temp[1].get_x(),temp[1].get_y())] + cost(temp[1].get_x(), temp[1].get_y(), next[0], next[1])

							if next not in cost_added or new_cost < cost_added[next]:
								#print "Added neighbor to queues"
								#if next not in closed_list or new_cost < cost_added[next]:
								cost_added[next] = new_cost		# g
								if next not in closed_list_anchor:
									myheuristic = self.heuristic(next[0], next[1], goalx, goaly, 0)
									priority0 = new_cost + myheuristic
									heuristic_list[0][next] = myheuristic
									priority_list[0][next] = priority0
									fringe[0].put(priority0, Coordinate(next[0],next[1],temp[1]))
									closed_list_anchor[next] = temp[1]
									if next not in closed_list:
										for j in range(1,5):
											myheuristic = self.heuristic(next[0], next[1], goalx, goaly, i+1)
											priority = new_cost + myheuristic
											if priority <= w2 * priority0:
												heuristic_list[i][next] = myheuristic
												priority_list[i][next] = priority
												fringe[i].put(priority, Coordinate(next[0],next[1],temp[1]))
												closed_list[next] = temp[1]
						#closed_list[temp[1]] = temp[1]

				else:
					#print "------------- Reached the else condition, using fringe[0] ---------------"
					if anchor[1].get_x() == goalx and anchor[1].get_y() == goaly:
							# Found goal, return path
							print "Made it to goal at " + str(goal[0]) + "," + str(goal[1])
							path_cost = 0
							# Make a straight path from goal to start
							PathNode = anchor[1]
							old_x = PathNode.get_x()
							old_y = PathNode.get_y()
							final_path.append((old_x,old_y))
							PathNode = PathNode.get_parent()

							while PathNode != None:
								path_cost += cost(PathNode.get_x(),PathNode.get_y(),old_x,old_y)
								final_path.append((PathNode.get_x(),PathNode.get_y()))
								#print "Path: " + str(current.get_x()) + "," + str(current.get_y())
								old_x = PathNode.get_x()
								old_y = PathNode.get_y()
								PathNode = PathNode.get_parent()
							#break
							return [closed_list,closed_list_anchor], cost_added, final_path, path_cost, priority_list, heuristic_list
					else:
						#print "-------------- adding to fringe[0] ---------------"
						for j in range(1,5):
							fringe[j].remove(anchor[1])

						# Expand
						for next in getNeighbors(anchor[1].get_x(), anchor[1].get_y()):
							#print "current x %d current y %d" % current[0], current[1]
							new_cost = cost_added[(anchor[1].get_x(),anchor[1].get_y())] + cost(anchor[1].get_x(), anchor[1].get_y(), next[0], next[1])

							if next not in cost_added or new_cost < cost_added[next]:
								#print "Added neighbor to queues"
								#if next not in closed_list or new_cost < cost_added[next]:
								cost_added[next] = new_cost		# g
								if next not in closed_list_anchor:
									myheuristic = self.heuristic(next[0], next[1], goalx, goaly, 0)
									priority0 = new_cost + myheuristic
									heuristic_list[0][next] = myheuristic
									priority_list[0][next] = priority0
									fringe[0].put(priority0, Coordinate(next[0],next[1],anchor[1]))
									closed_list_anchor[next] = anchor[1]
									if next not in closed_list:
										for j in range(1,5):
											myheuristic = self.heuristic(next[0], next[1], goalx, goaly, i+1)
											priority = new_cost + myheuristic
											if priority <= w2 * priority0:
												heuristic_list[i][next] = myheuristic
												priority_list[i][next] = priority
												fringe[i].put(priority, Coordinate(next[0],next[1],anchor[1]))
												closed_list_anchor[next] = anchor[1]
						#closed_list[anchor[1]] = anchor[1]
					anchor = fringe[0].getFull()


		return closed_list, cost_added, final_path, path_cost, priority_list, heuristic_list

# Main loop
running = True

GridSurface = pygame.Surface(GameScreen.get_size())

areacoordinates = makeGrid()
GridSurface = drawGrid(GridSurface)
start_x,start_y,goal_x,goal_y = generateStartFinish()
final_path = []
closed_list = []
cell_costs = []
priority_list = []
heuristic_list = []
path_cost = 0
elapsed_time = 0
drawmode = 0
nodes_expanded = 0

MySearch = AStarSearch() # Initialize Object

while(running):
	# Get Input
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				running = False
			elif event.key == pygame.K_g:
				grid = [['1' for y in range(GridRows)] for x in range(GridCols)]
				areacoordinates = makeGrid()
				GridSurface = drawGrid(GridSurface)
				start_x,start_y,goal_x,goal_y = generateStartFinish()
				final_path = []
				closed_list = []
				priority_list = []
				heuristic_list = []
				cell_costs = []
				path_cost = 0
				elapsed_time = 0
				nodes_expanded = 0
				print "Generated new map"
			elif event.key == pygame.K_e:
				start_x,start_y,goal_x,goal_y = generateStartFinish()
				final_path = []
				closed_list = []
				priority_list = []
				heuristic_list = []
				cell_costs = []
				path_cost = 0
				elapsed_time = 0
				nodes_expanded = 0
				print "Generated new start and finish points"
			elif event.key == pygame.K_s:
				# Save map: get filename
				filename = raw_input("Save map to: ")
				with open(os.path.join("./gen",filename),"w") as mapfile:
					mapfile.write(str((start_x,start_y)))		# Write start
					mapfile.write("\n")
					mapfile.write(str((goal_x,goal_y)))			# Write goal
					mapfile.write("\n")

					for area in areacoordinates:				# Write hard to traverse area centers
						mapfile.write(str((area[0],area[1])))
						mapfile.write("\n")

					for y in range(len(grid[x])):				# Write each cell
						for x in range(len(grid)):
							mapfile.write(str(grid[x][y]))
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
					new_goal = make_tuple(mapfile.readline())
					goal_x = new_goal[0]
					goal_y = new_goal[1]

					areacoordinates = []

					for i in range(8):
						new_area = make_tuple(mapfile.readline())
						areacoordinates.append((new_area[0],new_area[1]))

					for y in range(len(grid[x])):				# Read each cell
						for x in range(len(grid)):
							grid[x][y] = mapfile.read(1)
						mapfile.read(1)

					mapfile.close()
				final_path = []
				closed_list = []
				cell_costs = []
				priority_list = []
				heuristic_list = []
				path_cost = 0
				elapsed_time = 0
				nodes_expanded = 0
				GridSurface = drawGrid(GridSurface)
				print "Map loaded!"
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
			elif event.key == pygame.K_v:
				# draw closed list
				if drawmode == 0:
					drawmode = 1
				else:
					drawmode = 0
			elif event.key == pygame.K_a:		# -------- A* Search --------
				choice = -1
				while int(choice) < 1 or int(choice) > 6:
					choice = raw_input ("Enter (1) for Euclidean distance, (2) for Manhattan distance, (3) for Octile distance, (4) for Chebyshev distance, (5) for Straight-Diagonal Distance, or (6) Best/Minimum of all: ")
				MySearch = AStarSearch()
				start_time = time.time()
				closed_list, cell_costs, final_path, path_cost, priority_list, heuristic_list = MySearch.Search(start_x, start_y, goal_x, goal_y,choice)
				elapsed_time = time.time() - start_time
				nodes_expanded = len(closed_list)
			elif event.key == pygame.K_u:		# -------- Uniform Cost Search --------
				MySearch = UniformCostSearch()
				start_time = time.time()
				closed_list, cell_costs, final_path, path_cost, priority_list, heuristic_list = MySearch.Search(start_x, start_y, goal_x, goal_y)
				elapsed_time = time.time() - start_time
				nodes_expanded = len(closed_list)
			elif event.key == pygame.K_w:		# -------- Weighted A* Search --------
				choice = -1 #heuristic choice
				weight = 0 #weight of heuristic

				while (int(choice) < 1 or int(choice) > 6):
					choice = raw_input("Enter (1) for Euclidean distance, (2) for Manhattan Distance, (3) for Octile Distance, (4) for Chebyshev Distance, (5) for Straight-Diagonal Distance, or (6) Best/Minimum of all: ")
				while float(weight) < 1:
					weight = raw_input("Enter the selected weight for Weighted A* - must be >= 1: ")

				MySearch = WeightedAStarSearch(weight)
				start_time = time.time()
				closed_list, cell_costs, final_path, path_cost, priority_list, heuristic_list = MySearch.Search(start_x, start_y, goal_x, goal_y, choice)
				elapsed_time = time.time() - start_time

				nodes_expanded = len(closed_list)
			elif event.key == pygame.K_q:		# -------- Sequential A* Search --------
				#sequential search goes here
				print "Sequential Search"
				MySearch = SequentialAStarSearch()
				start_time = time.time()
				closed_lists, cell_costs, final_path, path_cost, priority_list, heuristic_list = MySearch.Search(start_x,start_y,goal_x, goal_y)
				elapsed_time = time.time() - start_time

				closed_list = []
				# Combine closed lists
				for list in closed_lists:
					for cell in list:
						if cell not in closed_list:
							closed_list.append(cell)
				nodes_expanded = len(closed_list)

			elif event.key == pygame.K_i:		# -------- Integrated A* Search --------
				#integrated search goes here
				print "Integrated Search"
				MySearch = IntegratedAStarSearch()
				start_time = time.time()
				closed_lists, cell_costs, final_path, path_cost, priority_list, heuristic_list = MySearch.Search(start_x,start_y,goal_x, goal_y)
				elapsed_time = time.time() - start_time

				closed_list = []
				# Combine closed lists
				for list in closed_lists:
					for cell in list:
						if cell not in closed_list:
							closed_list.append(cell)
				nodes_expanded = len(closed_list)


		drawScreen(GridSurface,closed_list,final_path,path_cost,nodes_expanded,drawmode,elapsed_time,cell_costs, priority_list, heuristic_list)

pygame.quit()
