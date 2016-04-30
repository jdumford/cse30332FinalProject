from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory, Protocol
from twisted.internet.task import LoopingCall
import pygame

SERVER_HOST = "student02.cse.nd.edu"
SERVER_PORT = 40073

class PlayerConnection(Protocol):
	def __init__(self,addr):
		self.line = 'no message'
		self.line2 = 'no message 2'
		self.addr = addr
		self.myturn = True

	def connectionMade(self):
		pygame.init()
		self.screen = pygame.display.set_mode((200, 200))
		reactor.callLater(.01,self.tick)

	def dataReceived(self,data):
		self.myturn = True
		self.line = data

	def connectionLost(self,reason):
		print "Connection lost to ",self.addr

	def tick(self):
		if self.myturn == True:
			self.screen.fill((0,0,0))
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					reactor.stop() # just stop somehow
				elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
					reactor.stop() # just stop somehow
				elif event.type == pygame.KEYDOWN:
					self.line = "KEYDOWN"
					self.myturn = False
					self.transport.write(self.line)
				elif event.type == pygame.MOUSEBUTTONDOWN:
					self.line2 = "MOUSEDOWN"
					self.myturn = False
					self.transport.write(self.line2)
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


