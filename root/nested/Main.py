'''
Created on 9 Sep 2012

@author: Callum
'''

from GameEngine import GameEngine
import pygame

if __name__ == '__main__':
    
    ### Start!
    pygameDisplay = pygame.display.set_mode((800, 600)) #Set screen size
    engine = GameEngine(pygameDisplay) #Create engine
    engine.run() #Get going....
    
    pass