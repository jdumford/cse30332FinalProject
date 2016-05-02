import pygame
from spritesheet import spritesheet
from pygame.locals import *
import numpy


"""1 is water, 2 is ship, 3 is HIT, 4 is miss"""
class Board(object):
	def __init__(self):
		self.Matrix = [[1 for x in range(10)] for y in range(10)]
	
	def setSpace(self,x,y,new):
		if new == 2: #ship
			self.Matrix[y][x] = new
			self.Matrix[y+1][x] = new
			self.Matrix[y+2][x] = new
		elif new == 3: #HIT
			self.Matrix[y][x] = 3
		elif new == 4: #MISS
			self.Matrix[y][x] = 4
		for i in range(0,10):
			for j in range(0,10):
				print self.Matrix[j][i],
			print ""
	def getSpace(self,x,y):
		return self.Matrix[y][x]
		

