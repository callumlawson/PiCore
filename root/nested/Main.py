'''
Created on 9 Sep 2012

@author: Callum
'''

from GameEngine import GameEngine
import pygame
from pygame.locals import *

if __name__ == '__main__':
    
    ### Start!
    pygameDisplay=pygame.display.set_mode((800,800),HWSURFACE|RESIZABLE)
    pygame.display.set_caption("PiCore")
    engine = GameEngine(pygameDisplay) #Create engine
    engine.run() #Get going....
    
    pass