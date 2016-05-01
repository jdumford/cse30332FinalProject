from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory, Protocol
from twisted.internet.task import LoopingCall
import pygame
import cmath
from spritesheet import spritesheet
from board import Board

SERVER_HOST = "student02.cse.nd.edu"
SERVER_PORT = 40073

class PlayerConnection(Protocol):
	def __init__(self,addr):
		self.addr = addr
		self.img_size = 33
		self.ship_counter = 0
		self.board1 = Board()
		self.board2 = Board()
		self.myturn = True	

	def connectionMade(self):
		"""initialize game, screen, sheets to be displayed, image lists, and callLater function"""
		pygame.init()
		self.screen = pygame.display.set_mode(((self.img_size+1)*10, (self.img_size+1)*10))
		watersheet = spritesheet("sprites/water.png")
		self.water = watersheet.image_at((50, 50, self.img_size, self.img_size))
		boatsheet = spritesheet("sprites/battleships.png")
		self.battleship = boatsheet.image_at((93, 130, self.img_size, 100))
		
		reactor.callLater(.01,self.tick)

	def dataReceived(self,data):
		"""Receive mouse position of opponent's missle fire"""
		self.myturn = True
		str_data = data.split()
		x_pos = str_data[0]
		y_pos = str_data[1]
		self.determineOutcome(float(x_pos),float(y_pos))
	
	def connectionLost(self,reason):
		print "Connection lost to ",self.addr

	def determineOutcome(x_old,y_old):
		"""calculate x,y position on 10x10 board, check spot type, perform appropriate action"""
		x_new = int(math.floor(x_old/33))
		y_new = int(math.floor(y_old/33))
		space_type = self.board.getSpace(x_new,y_new)
		if space_type == 1:
			#Spot is water and MISS
			pass
		elif space_type == 2:
			#Space type is a hip and HIT, replace sprite with ship
			pass

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
				elif event.type == pygame.MOUSEMOTION and self.ship_counter < 1:
					mx, my = pygame.mouse.get_pos()
				elif event.type == pygame.MOUSEBUTTONDOWN:
					#valid spot then send coordinates with additional 250 so changes occur on opponent side of board; elif place boat
					mx, my = pygame.mouse.get_pos()
					if my < 165:
						print "Clicked enemy area"
						my = my + 165
						self.myturn = False
						self.transport.write(str(mx) + ' ' + str(my))
					elif my > 165:
						print "Clicked home area"
						self.ship_counter = self.ship_counter + 1
			#render player 2 side of board
			for x in range (0,5):
				for y in range(0,10):
					if self.board2.getSpace(x,y) == 1:
						self.screen.blit(self.water, ((self.img_size+1)*x, (self.img_size+1)*y))
			#render player 1 side of board
			for x in range (5,10):
				for y in range(0,10):
					if self.board1.getSpace(x,y) == 1:
						self.screen.blit(self.water, ((self.img_size+1)*x, (self.img_size+1)*y))
			if self.ship_counter < 1:
				self.screen.blit(self.battleship, (mx, my))				
			#screen.blit(self.board1.fire, (self.board1.img_size+1, self.board1.img_size+1))
			#screen.blit(self.board1.battleship, (mx,my))
			pygame.display.flip()
			pygame.display.set_caption("Player 1")
			reactor.callLater(1,self.tick)


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


