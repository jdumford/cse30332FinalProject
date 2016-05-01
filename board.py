import pygame
from spritesheet import spritesheet
from pygame.locals import *
import numpy

class Board(object):
	def __init__(self):
		self.Matrix = [[1 for x in range(10)] for y in range(10)]
	
	def setSpace(self,x,y,new):
		self.Matrix[y][x] = new

	def getSpace(self,x,y):
		return self.Matrix[y][x]
		

