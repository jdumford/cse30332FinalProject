from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory, Protocol
from twisted.internet.task import LoopingCall
import pygame
import math
from spritesheet import spritesheet
from board import Board

SERVER_HOST = "student02.cse.nd.edu"
SERVER_PORT = 41073

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
		self.board2 = Board()
		self.board2 = Board()
		self.myturn = True
		self.set = False
		self.changeboard = False
		#self.sendboard = False
		self.win = False
		self.lose = False

	def connectionMade(self):
		"""initialize game, screen, sheets to be displayed, image lists, and callLater function"""
		pygame.init()
		self.screen = pygame.display.set_mode(((self.img_size+1)*10, (self.img_size+1)*10))
		watersheet = spritesheet("sprites/water.png")
		self.water = watersheet.image_at((50, 50, self.img_size, self.img_size))
		firesheet = spritesheet("sprites/fire.png")
		self.fire = firesheet.image_at((415, 22, self.img_size, self.img_size))
		misssheet = spritesheet("sprites/miss.png")
		self.miss = misssheet.image_at((455, 182, self.img_size, self.img_size))
		boatsheet = spritesheet("sprites/battleships.png")
		self.battleship = boatsheet.image_at((93, 130, self.img_size, 100))
                self.battleship1 = boatsheet.image_at((93, 130, self.img_size, 100))
                self.battleship2 = boatsheet.image_at((249, 128, self.img_size, 67))
                self.battleship3 = boatsheet.image_at((93, 130, self.img_size, 100))
                self.battleship3 = pygame.transform.rotate(self.battleship3, 90)
                self.battleship4 = boatsheet.image_at((249, 128, self.img_size, 67))
                self.battleship4 = pygame.transform.rotate(self.battleship4, 90)
		self.win_image = pygame.image.load("sprites/win.png").convert()
		self.lose_image = pygame.image.load("sprites/lose.png").convert()
		
		reactor.callLater(.01,self.tick)

	def dataReceived(self,data):
		"""Receive "ready to start" and mouse position of opponent's missle fire"""
		if len(data) > 10:
			#self.myturn = False
			#self.changeboard = True
			#self.sendboard = True
			#reactor.callLater(.01,self.tick)
		#elif self.changeboard == True:
			str_data = data.split()
			for i in range(0, width):
				for j in range(0, height/2):
					x = float(str_data[(i*(height/2)) + j])
					if x ==2:
						self.board2.setSpace(i,j, 5)
			#self.changeboard = False
                        reactor.callLater(.01,self.tick)
		elif data == "end game":
			self.myturn = True
			self.lose = True
			print "Player 2, you lose..."
			self.tick()
		else:
			self.myturn = True
			str_data = data.split()
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
		space_type = self.board2.getSpace(x_new,y_new)
		if space_type == 1:
			#Spot is water and MISS
			self.board2.setSpace(x_new,y_new,4)
			return True
		elif space_type == 2 or space_type == 5:
			#Space type is a hip and HIT, replace sprite with ship
			self.board2.setSpace(x_new,y_new,3)
			return True
		return False

	def tick(self):
		if self.changeboard == True:
			data_str = ''
			for i in range(0, width):
				for j in range(height/2, height):
					data_str = data_str + ' ' + str(self.board2.getSpace(i, j))
			self.changeboard = False
			self.myturn = False
			self.transport.write(data_str)

		elif self.myturn == True:
			self.screen.fill((0,0,0))			
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					reactor.stop() # just stop somehow
				elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
					reactor.stop() # just stop somehow
				#placing initial ships, get mouse position
				elif event.type == pygame.MOUSEMOTION and self.ship_counter < 4:
					self.mx, self.my = pygame.mouse.get_pos()
				elif event.type == pygame.MOUSEBUTTONDOWN:
					#valid spot then send coordinates with additional 165 so changes 
					#occur on opponent side of board; elif place ships 1,2,3
					self.mx, self.my = pygame.mouse.get_pos()
					if self.my < pxh/2 and self.ship_counter == 4:
						if(self.determineOutcome(self.mx, self.my)):
							self.my = self.my + pxh/2
							self.myturn = False
							if self.board2.checkWin() is True:
								print 'Player 2, you win!'
								self.win = True
								self.transport.write("end game")
							else:
								self.transport.write(str(self.mx) + ' ' + str(self.my))
					elif self.my > pxh/2 and self.ship_counter == 0:
						self.ship1_x = int(math.floor(self.mx/(ipx+1))) * (ipx+1)
						self.ship1_y = int(math.floor(self.my/(ipx+1))) * (ipx+1)
						x = int(math.floor(self.mx/(ipx+1)))
						y = int(math.floor(self.my/(ipx+1)))
						if y < height - 2:
							self.board2.setSpace(x,y,2)
							self.board2.setSpace(x,y+1,2)
							self.board2.setSpace(x,y+2,2)
							self.ship_counter = self.ship_counter + 1
					elif self.my > pxh/2 and self.ship_counter == 1:
						self.ship2_x = int(math.floor(self.mx/(ipx+1))) * (ipx+1)
						self.ship2_y = int(math.floor(self.my/(ipx+1))) * (ipx+1)
						x = int(math.floor(self.mx/(ipx+1)))
						y = int(math.floor(self.my/(ipx+1)))
						if y < height - 1 and self.board2.getSpace(x,y) == 1 and self.board2.getSpace(x,y+1) == 1:
							self.board2.setSpace(x,y,2)
							self.board2.setSpace(x,y+1,2)
							self.ship_counter = self.ship_counter + 1
					elif self.my > pxh/2 and self.ship_counter == 2:
						self.ship3_x = int(math.floor(self.mx/(ipx+1))) * (ipx+1)
						self.ship3_y = int(math.floor(self.my/(ipx+1))) * (ipx+1)
						x = int(math.floor(self.mx/(ipx+1)))
						y = int(math.floor(self.my/(ipx+1)))
						if x < width - 2 and self.board2.getSpace(x,y) == 1 and self.board2.getSpace(x+1,y) == 1 and self.board2.getSpace(x+2,y) == 1:
							self.board2.setSpace(x,y,2)
							self.board2.setSpace(x+1,y,2)
							self.board2.setSpace(x+2,y,2)
							self.ship_counter = self.ship_counter + 1
					elif self.my > pxh/2 and self.ship_counter == 3:
						self.ship4_x = int(math.floor(self.mx/(ipx+1))) * (ipx+1)
						self.ship4_y = int(math.floor(self.my/(ipx+1))) * (ipx+1)
						x = int(math.floor(self.mx/(ipx+1)))
						y = int(math.floor(self.my/(ipx+1)))
						if x < width - 1 and self.board2.getSpace(x,y) == 1 and self.board2.getSpace(x+1,y) == 1:
							self.board2.setSpace(x,y,2)
							self.board2.setSpace(x+1,y,2)
							self.ship_counter = self.ship_counter + 1
							self.changeboard = True

			#fill everythin up with water image
			for x in range (0,width):
				for y in range(0,height):
					if self.board2.getSpace(x,y) == 1 or self.board2.getSpace(x,y) == 5:
						self.screen.blit(self.water, ((ipx+1)*x, (ipx+1)*y))

			#show moving ship
			if self.ship_counter == 0:
				self.screen.blit(self.battleship, (self.mx, self.my))
			#on clicks, ships are placed
			if self.ship_counter == 1:
				self.screen.blit(self.battleship1, (self.ship1_x,self.ship1_y))
                                self.screen.blit(self.battleship2, (self.mx, self.my))
                        elif self.ship_counter == 2:
                                self.screen.blit(self.battleship1, (self.ship1_x,self.ship1_y))
                                self.screen.blit(self.battleship2, (self.ship2_x,self.ship2_y))
                                self.screen.blit(self.battleship3, (self.mx, self.my))
                        elif self.ship_counter == 3:
                                self.screen.blit(self.battleship1, (self.ship1_x,self.ship1_y))
                                self.screen.blit(self.battleship2, (self.ship2_x,self.ship2_y))
                                self.screen.blit(self.battleship3, (self.ship3_x,self.ship3_y))
                                self.screen.blit(self.battleship4, (self.mx, self.my))
                        elif self.ship_counter == 4:
                                self.screen.blit(self.battleship1, (self.ship1_x,self.ship1_y))
                                self.screen.blit(self.battleship2, (self.ship2_x,self.ship2_y))
                                self.screen.blit(self.battleship3, (self.ship3_x,self.ship3_y))
                                self.screen.blit(self.battleship4, (self.ship4_x,self.ship4_y))

			#Overwrite water and ship with fire image
			for x in range (0,width):
				for y in range(0,height):
					if self.board2.getSpace(x,y) == 3:
						self.screen.blit(self.fire, ((ipx+1)*x, (ipx+1)*y))
					if self.board2.getSpace(x,y) == 4:
						self.screen.blit(self.miss, ((ipx+1)*x, (ipx+1)*y))

			if self.win == True:
				self.screen.blit(self.win_image, (20, 100))
				self.myturn = False
			if self.lose == True:
				self.screen.blit(self.lose_image, (20,100))
				self.myturn = False

			pygame.display.flip()
			pygame.display.set_caption("Player 2")
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


