from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory, Protocol
from twisted.internet.task import LoopingCall
import pygame
import math
from spritesheet import spritesheet
from board import Board

SERVER_HOST = "student02.cse.nd.edu"
SERVER_PORT = 40073

height = 10
width = 10
#image pixels
ipx = 33
#height in pixels
pxh = height * (ipx+1)


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
		self.mx = 0
		self.my = 0
		self.board1 = Board()
		self.board2 = Board()
		self.myturn = True
		self.set = False
		self.changeboard = False

	def connectionMade(self):
		"""initialize game, screen, sheets to be displayed, image lists, and callLater function"""
		pygame.init()
		self.screen = pygame.display.set_mode(((self.img_size+1)*10, (self.img_size+1)*10))
		watersheet = spritesheet("sprites/water.png")
		self.water = watersheet.image_at((50, 50, self.img_size, self.img_size))
		firesheet = spritesheet("sprites/fire.png")
		self.fire = firesheet.image_at((415, 22, self.img_size, self.img_size))
		boatsheet = spritesheet("sprites/battleships.png")
		self.battleship = boatsheet.image_at((93, 130, self.img_size, 100))
		self.battleship1 = boatsheet.image_at((93, 130, self.img_size, 100))
		self.battleship2 = boatsheet.image_at((93, 130, self.img_size, 100))
		self.battleship3 = boatsheet.image_at((93, 130, self.img_size, 100))	
		

		reactor.callLater(.01,self.tick)

	def dataReceived(self,data):
		"""Receive "ready to start" and mouse position of opponent's missle fire"""
		print "Data received from P2 is {0}".format(data)
		if len(data) > 10:
			self.myturn = True
			#self.changeboard = True
			#reactor.callLater(.01,self.tick)
		#elif self.changeboard == True:
			str_data = data.split()
			print str_data
			for i in range(0, width):
				for j in range(0, height/2):
					x = float(str_data[(i*(height/2)) + j])
					print x
					if x == 2:
						print "HERE!!!!!!!!"
						self.board1.setSpace(i, j, 5)
			reactor.callLater(.01,self.tick)
		else:
			self.myturn = True
			str_data = data.split()
			print str_data
			x_pos = str_data[0]
			y_pos = str_data[1]
			self.determineOutcome(float(x_pos),float(y_pos))
			reactor.callLater(.01,self.tick)
	
	def connectionLost(self,reason):
		print "Connection lost to ",self.addr

	def determineOutcome(self,x_old,y_old):
		"""calculate x,y position on 10x10 board, check spot type, perform appropriate action"""
		x_new = int(math.floor(x_old/(ipx+1)))
		y_new = int(math.floor(y_old/(ipx+1)))
		print "xnew and ynew = {0} {1}".format(x_new,y_new)
		space_type = self.board1.getSpace(x_new,y_new)
		print "space type = {0}".format(space_type)
		if space_type == 1:
			#Spot is water and MISS
			self.board1.setSpace(x_new,y_new,4)
		elif space_type == 2 or space_type == 5:
			#Space type is a hip and HIT, replace sprite with ship
			self.board1.setSpace(x_new,y_new,3)

	def tick(self):
		if self.changeboard == True:
			data_str = ''
			for i in range(0, width):
				for j in range(height/2, height):
					data_str = data_str + ' ' + str(self.board1.getSpace(j, i))
			self.transport.write(data_str)
			self.changeboard = False

		elif self.myturn == True:
			self.screen.fill((0,0,0))			
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					reactor.stop() # just stop somehow
				elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
					reactor.stop() # just stop somehow
				#placing initial ships, get mouse position
				elif event.type == pygame.MOUSEMOTION and self.ship_counter < 3:
					self.mx, self.my = pygame.mouse.get_pos()
				elif event.type == pygame.MOUSEBUTTONDOWN:
					#valid spot then send coordinates with additional 165 so changes 
					#occur on opponent side of board; elif place ships 1,2,3
					self.mx, self.my = pygame.mouse.get_pos()
					if self.my < pxh/2 and self.ship_counter == 3:
						print "Clicked enemy area"
						self.determineOutcome(self.mx, self.my)
						self.my = self.my + pxh/2
						self.myturn = False
						self.transport.write(str(self.mx) + ' ' + str(self.my))
					elif self.my > pxh/2 and self.ship_counter == 0:
						print "Placing ship 1"
						self.ship1_x = int(math.floor(self.mx/(ipx+1))) * (ipx+1)
						self.ship1_y = int(math.floor(self.my/(ipx+1))) * (ipx+1)
						x = int(math.floor(self.mx/(ipx+1)))
						y = int(math.floor(self.my/(ipx+1)))
						self.board1.setSpace(x,y,2)
						self.ship_counter = self.ship_counter + 1
					elif self.my > pxh/2 and self.ship_counter == 1:
						print "Placing ship 2"
						self.ship2_x = int(math.floor(self.mx/(ipx+1))) * (ipx+1)
						self.ship2_y = int(math.floor(self.my/(ipx+1))) * (ipx+1)
						x = int(math.floor(self.mx/(ipx+1)))
						y = int(math.floor(self.my/(ipx+1)))
						self.board1.setSpace(x,y,2)
						self.ship_counter = self.ship_counter + 1
					elif self.my > pxh/2 and self.ship_counter == 2:
						print "Placing ship 3"
						self.ship3_x = int(math.floor(self.mx/(ipx+1))) * (ipx+1)
						self.ship3_y = int(math.floor(self.my/(ipx+1))) * (ipx+1)
						x = int(math.floor(self.mx/(ipx+1)))
						y = int(math.floor(self.my/(ipx+1)))
						self.board1.setSpace(x,y,2)
						self.ship_counter = self.ship_counter + 1
						#self.transport.write("ready")
						self.set = True
						print "Waiting for player 2 to set pieces"
						self.changeboard = True
						
			#fill everythin up with water image
			for x in range (0,width):
				for y in range(0,height):
					if self.board1.getSpace(x,y) == 1 or self.board1.getSpace(x,y) == 5:
						self.screen.blit(self.water, ((ipx+1)*x, (ipx+1)*y))

			#show moving ship
			if self.ship_counter < 3:
				self.screen.blit(self.battleship, (self.mx, self.my))
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
			for x in range (0,width):
				for y in range(0,height):
					if self.board1.getSpace(x,y) == 3:
						self.screen.blit(self.fire, ((ipx+1)*x, (ipx+1)*y))

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


