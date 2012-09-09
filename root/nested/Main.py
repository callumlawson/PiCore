'''
Created on 7 Sep 2012

@author: Callum
'''
import pygame, sys
from pygame.locals import *



import Parser

if __name__ == '__main__':
    
    #Init
    pygame.init()
    fpsClock = pygame.time.Clock()
    windowSurfaceObj = pygame.display.set_mode((640,480))
    pygame.display.set_caption('Pi Core')
    mousex, mousey = 0,0
    
    whiteColor = pygame.Color(255,255,255)
    redColor = pygame.Color(255,0,0)    
    sdtFont = pygame.font.Font('freesansbold.ttf', 32)
    
    #Parser
    parser = Parser.Parser()
    for instruction in  parser.processFile("demoCode.txt"):
        print instruction.printInstruction()
    
    #Main game loop
    while True:
        windowSurfaceObj.fill(whiteColor)
        pygame.draw.rect(windowSurfaceObj,redColor,(100,100,100,100))
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex,mousey = event.pos
        
        pygame.display.update()
     
    pass