'''
Created on 7 Sep 2012

@author: Callum
'''
import sys
sys.path.insert(0, '..')

import pygame
from pygame.locals import *
from pgu import gui

import Parser 

if __name__ == '__main__':
    
    #Init
    pygame.init()
    fpsClock = pygame.time.Clock()
    windowSurfaceObj = pygame.display.set_mode((640,480),SWSURFACE)
    pygame.display.set_caption('Pi Core')
    mousex, mousey = 0,0
    
    whiteColor = pygame.Color(255,255,255)
    redColor = pygame.Color(255,0,0)    
    sdtFont = pygame.font.Font('freesansbold.ttf', 32)
    
    #Parser
    parser = Parser.Parser()
    for instruction in  parser.processFile("demoCode.txt"):
        print instruction.printInstruction()
        
    #Init GUI
    app = gui.App()
    app.connect(gui.QUIT, app.quit)
       
    buttonTest = gui.Button("Quit")
    container = gui.Table(width=0,height=0)
    
    container.add(buttonTest, 0 ,0)
    app.run(container)
    
        
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
                
            elif event.type == MOUSEBUTTONUP:
                mousex,mousey = event.pos
                if event.button in (1,2,3):
                    print 'left, middle, or right mouse released'
                elif event.button in (4,5):
                    print 'mouse scrolled up or down'
        
        pygame.display.update()
     
    pass