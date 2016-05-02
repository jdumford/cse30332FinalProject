from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory, Protocol
from twisted.internet.task import LoopingCall
import pygame
import math
from spritesheet import spritesheet
from board import Board

SERVER_HOST = "student02.cse.nd.edu"
SERVER_PORT = 40073

class PlayerConnection(Protocol):
	def __init__(self,addr):
		self.addr = addr
		self.img_size = 33
		self.ship_counter = 0
		self.ship1_x = 0
		self.ship1_y = 0
		self.ship2_x = 0
		self.ship2_y = 0
		self.ship3_x = 0
		self.ship3_y = 0
		self.board1 = Board()
		self.board2 = Board()
		self.myturn = True	

	def connectionMade(self):
		"""initialize game, screen, sheets to be displayed, image lists, and callLater function"""
		pygame.init()
		self.screen = pygame.display.set_mode(((self.img_size+1)*10, (self.img_size+1)*10))
		watersheet = spritesheet("sprites/water.png")
		self.water = watersheet.image_at((50, 50, self.img_size, self.img_size))
		firesheet = spritesheet("sprites/fire.png")
		self.fire = firesheet.image_at((50, 50, self.img_size, self.img_size))
		boatsheet = spritesheet("sprites/battleships.png")
		self.battleship = boatsheet.image_at((93, 130, self.img_size, 100))
		self.battleship1 = boatsheet.image_at((93, 130, self.img_size, 100))
		self.battleship2 = boatsheet.image_at((93, 130, self.img_size, 100))
		self.battleship3 = boatsheet.image_at((93, 130, self.img_size, 100))	
		

		reactor.callLater(.01,self.tick)

	def dataReceived(self,data):
		"""Receive "ready to start" and mouse position of opponent's missle fire"""
		print "Data received from P2 is {0}".format(data)
		if data == "ready":
			self.myturn = True
		else:
			self.myturn = True
			str_data = data.split()
			x_pos = str_data[0]
			y_pos = str_data[1]
			self.determineOutcome(float(x_pos),float(y_pos))
	
	def connectionLost(self,reason):
		print "Connection lost to ",self.addr

	def determineOutcome(self,x_old,y_old):
		"""calculate x,y position on 10x10 board, check spot type, perform appropriate action"""
		x_new = int(math.floor(x_old/34))
		y_new = int(math.floor(y_old/34))
		print "xnew and ynew = {0} {1}".format(x_new,y_new)
		space_type = self.board1.getSpace(x_new,y_new)
		print "space type = {0}".format(space_type)
		if space_type == 1:
			#Spot is water and MISS
			self.board1.setSpace(x_new,y_new,4)
		elif space_type == 2:
			#Space type is a hip and HIT, replace sprite with ship
			self.board1.setSpace(x_new,y_new,3)

	def tick(self):
		if self.myturn == True:
			mx, my = 0,0
			self.screen.fill((0,0,0))			
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					reactor.stop() # just stop somehow
				elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
					reactor.stop() # just stop somehow
				#placing initial ships, get mouse position
				elif event.type == pygame.MOUSEMOTION and self.ship_counter < 3:
					mx, my = pygame.mouse.get_pos()
				elif event.type == pygame.MOUSEBUTTONDOWN:
					#valid spot then send coordinates with additional 165 so changes occur on opponent side of board; elif place ships 1,2,3
					mx, my = pygame.mouse.get_pos()
					if my < 170 and self.ship_counter == 3:
						print "Clicked enemy area"
						my = my + 170
						#self.myturn = False
						self.transport.write(str(mx) + ' ' + str(my))
					elif my > 170 and self.ship_counter == 0:
						print "Placing ship 1"
						self.ship1_x = int(math.floor(mx/34)) * 34
						self.ship1_y = int(math.floor(my/34)) * 34
						x = int(math.floor(mx/34))
						y = int(math.floor(my/34))
						self.board1.setSpace(x,y,2)
						self.ship_counter = self.ship_counter + 1
					elif my > 170 and self.ship_counter == 1:
						print "Placing ship 2"
						self.ship2_x = int(math.floor(mx/34)) * 34
						self.ship2_y = int(math.floor(my/34)) * 34
						x = int(math.floor(mx/34))
						y = int(math.floor(my/34))
						self.board1.setSpace(x,y,2)
						self.ship_counter = self.ship_counter + 1
					elif my > 170 and self.ship_counter == 2:
						print "Placing ship 3"
						self.ship3_x = int(math.floor(mx/34)) * 34
						self.ship3_y = int(math.floor(my/34)) * 34
						x = int(math.floor(mx/34))
						y = int(math.floor(my/34))
						self.board1.setSpace(x,y,2)
						self.ship_counter = self.ship_counter + 1
						self.transport.write("ready")
						print "Waiting for player 2 to set pieces"
						#self.myturn = False
						
			#fill everythin up with water image
			for x in range (0,10):
				for y in range(0,10):
					if self.board1.getSpace(x,y) == 1:
						self.screen.blit(self.water, ((self.img_size+1)*x, (self.img_size+1)*y))

			#show moving ship
			if self.ship_counter < 3:
				self.screen.blit(self.battleship, (mx, my))
			#on clicks, ships are placed
			if self.ship_counter == 1:
				self.screen.blit(self.battleship1, (self.ship1_x,self.ship1_y))
			elif self.ship_counter == 2:
				self.screen.blit(self.battleship1, (self.ship1_x,self.ship1_y))
				self.screen.blit(self.battleship2, (self.ship2_x,self.ship2_y))
			elif self.ship_counter == 3:
				self.screen.blit(self.battleship1, (self.ship1_x,self.ship1_y))
				self.screen.blit(self.battleship2, (self.ship2_x,self.ship2_y))	
				self.screen.blit(self.battleship3, (self.ship3_x,self.ship3_y))

			#Overwrite water and ship with fire image
			for x in range (0,10):
				for y in range(0,10):
					if self.board1.getSpace(x,y) == 3:
						self.screen.blit(self.fire, ((self.img_size+1)*x, (self.img_size+1)*y))						

			pygame.display.flip()
			pygame.display.set_caption("Player 1")
			reactor.callLater(.01,self.tick)


class PlayerConnectionFactory(ClientFactory):
	def __init__(self):
		pass

	def buildProtocol(self,addr):
		return PlayerConnection(addr)

if __name__ == '__main__':
	player = PlayerConnectionFactory()
	#player = LoopingCall(c.tick)
	#lc.start(0.1)
	reactor.connectTCP(SERVER_HOST,SERVER_PORT,player)
	reactor.run()


