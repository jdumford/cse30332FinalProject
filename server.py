#Jacob Dumford and David Lewis
#Programming Paradigms Final Project
#Server file for our battleship game

import sys
import os
import math
import pygame
from pygame.locals import *

from twisted.internet.protocol import Factory
from twisted.internet.protocol import Protocol
from twisted.internet.protocol import ClientFactory
from twisted.internet import reactor
from twisted.internet.defer import DeferredQueue
#from twisted.internet.task import LoopingCall

P1_PORT = 40073
P2_PORT = 41073


#class to handle the connection to player 1
class P1Connection(Protocol):
    def __init__(self, addr):
        self.addr = addr

    def connectionMade(self):
        print 'Player 1 now connected'
        reactor.listenTCP(P2_PORT, P2ConnectionFactory(self))

    def dataReceived(self, data):
        print 'Data received from Player 1'
        self.p2.transport.write(data)

    def connectionLost(self, reason):
        print 'Connection with Player 1 lost for reason: ', reason

class P1ConnectionFactory(Factory):
    def buildProtocol(self, addr):
        return P1Connection(addr)


class P2Connection(Protocol):
    def __init__(self, addr, p1):
        self.addr = addr
        self.p1 = p1
        self.p1.p2 = self

    def connectionMade(self):
        print 'Player 2 now connected'

    def dataReceived(self, data):
        print 'Data received from Player 2'
        self.p1.transport.write(data)

    def connectionLost(self, reason):
        print 'Connection with Player 2 lost for reason: ', reason

class P2ConnectionFactory(Factory):
    def __init__(self, p1):
        self.p1 = p1
    def buildProtocol(self, addr):
        return P2Connection(addr, self.p1)




if __name__ == '__main__':
    reactor.listenTCP(P1_PORT, P1ConnectionFactory())
    reactor.run()
