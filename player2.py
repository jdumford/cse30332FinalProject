from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory, Protocol
from twisted.internet.task import LoopingCall
import pygame
import cmath
from board import Board

SERVER_PORT = 41073
SERVER_HOST = "student02.cse.nd.edu"

class PlayerConnection(Protocol):
	def __init__(self,addr):
		self.line = 'no message'
		self.line2 = 'no message 2'
		self.board1 = Board()
		self.board2 = Board()
		self.addr = addr
		self.myturn = True

	def connectionMade(self):
		pygame.init()
		self.screen = pygame.display.set_mode((500, 500))
		reactor.callLater(.01,self.tick)

	def dataReceived(self,data):
		"""Receive mouse position of opponent's missle fire"""
		self.myturn = True
		str_data = data.split()
		x_pos = str_data[0]
		y_pos = str_data[1]
		self.determineOutcome(x_pos,y_pos)
		
#		self.line = data
	def determineOutcome(x_old,y_old):
		"""calculate x,y position on 10x10 board, check spot type, perform appropriate action"""
		x_new = int(math.floor(x_old*2/100))
		y_new = int(math.floor(y_old*2/100))
		space_type = self.board2.getSpace(x_new,y_new)
		if space_type == 1:
			#Spot is water and MISS; replace water with miss sprite
			pass
		elif space_type == 2:
			#Spot is a ship and HIT; replace sprite with ship
			pass

	def connectionLost(self,reason):
		print "Connection lost to ",self.addr

	def tick(self):
		if self.myturn == True:
			self.screen.fill((0,0,0))
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					reactor.stop()# just stop somehow
				elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
					reactor.stop() # just stop somehow
				elif event.type == pygame.MOUSEBUTTONDOWN:
					#valid spot then send coordinates with additional 250 so changes occur on opponent side of board
					mx, my = pygame.mouse.get_pos()
					if my < 250:
						my = my + 250
						self.myturn = False
						self.transport.write(str(mx) + ' ' + str(my))

			self.screen.blit(pygame.font.SysFont('mono', 12, bold=True).render(self.line, True, (0, 255, 0)), (20,20))
			self.screen.blit(pygame.font.SysFont('mono', 12, bold=True).render(self.line2, True, (0, 255, 0)), (30,30))
			pygame.display.flip()
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


