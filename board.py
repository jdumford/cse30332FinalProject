import pygame
from spritesheet import spritesheet
from pygame.locals import *
import numpy


"""1 is water, 2 is ship, 3 is HIT, 4 is miss, 5 is opponent ship"""
class Board(object):
	def __init__(self):
		self.Matrix = [[1 for x in range(10)] for y in range(10)]
		self.opp_ship_spaces = 9
	
	def setSpace(self,x,y,new):
		current_space  = self.Matrix[y][x]
		if new == 2: #ship
			self.Matrix[y][x] = new
			self.Matrix[y+1][x] = new
			self.Matrix[y+2][x] = new
		elif new == 3 and current_space == 5:
			self.Matrix[y][x] = new
			self.opp_ship_spaces -= 1
		else:
			self.Matrix[y][x] = new
		
		for i in range(0,10):
			for j in range(0,10):
				print self.Matrix[i][j],
			print ""
	
	def getSpace(self,x,y):
		return self.Matrix[y][x]
		
	def checkWin(self):
		if self.opp_ship_spaces == 0:
			return True
		else:
			return False





