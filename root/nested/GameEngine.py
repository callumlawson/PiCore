'''
Created on 9 Sep 2012

@author: Callum
'''

import pygame
import time
import math
import pgu
from pgu import gui, timer
from GUI import MainGui
from Parser import Parser

class GameEngine(object):
    
    #Global
    screenWidth,screenHeight = 0,0
    numAddresses = 50
    squareSize = 5
    padding = 5
    display = None
    drawArea = None
    
    def __init__(self, pygameDisplay):
        
        self.display = pygameDisplay
        self.screenWidth = pygame.display.Info().current_w
        self.screenHeight = pygame.display.Info().current_h
        
        #Parser
        parser = Parser()
        for instruction in  parser.processFile("demoCode.txt"):
            print instruction.printInstruction()
    
        self.drawArea = pygame.Surface((self.screenWidth,self.screenHeight)).convert_alpha()
        self.drawArea.fill((120,120,120))
        
        self.app = MainGui(self.display)
        self.app.engine = self

    # Pause the game clock
    def pause(self):
        self.clock.pause()

    # Resume the game clock
    def resume(self):
        self.clock.resume()

    def render(self, dest, rect): #Do the drawing stuff!
        
        # Draw a rotating drawArea
        #angle = self.clock.get_time()*10
        #r = surf.get_rect()
        #r.center = rect.center
        #dest.fill((0,0,0), rect)
        #angle = 90
        #surf = pygame.transform.rotozoom(self.drawArea, angle, 1)
        
        print self.screenWidth
        pygame.draw.rect(self.drawArea,pygame.Color(0,255,0),(0,0,self.screenWidth,self.screenHeight))
        
        #Find screen space area. 
        self.squareSize = math.floor(math.sqrt((self.screenWidth*self.screenHeight)/self.numAddresses))#Will be run on pygame.VIDEORESIZE event to improve performance
        
        #print int(math.floor(self.screenWidth/(self.squareSize+self.padding)))
        count = 0
        while(count!=self.numAddresses):
            for x in xrange(int(math.ceil(self.screenWidth/(self.squareSize+self.padding)))):
                for y in xrange(int(math.ceil(self.screenHeight/(self.squareSize+self.padding)))):
                    count+=1
                    pygame.draw.rect(self.drawArea,pygame.Color(200,200,200) ,(x*(self.squareSize + self.padding),y*(self.squareSize + self.padding),self.squareSize,self.squareSize), 0)
            print "error not enough addresses drawn"
            break 
        
        self.display.blit(self.drawArea,(0,0))

        return (rect,)

    def run(self):
        self.app.update()
        pygame.display.flip()

        self.font = pygame.font.SysFont("", 16)

        self.clock = timer.Clock() #pygame.time.Clock()
        
        # Main program loop
        done = False
        while not done:
            # Process events
            for event in pygame.event.get():
                if (event.type == pygame.QUIT or 
                    event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    done = True
                    
                if event.type == pygame.VIDEORESIZE:
                    self.display = pygame.display.set_mode(event.dict['size'],pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE)
                    self.drawArea = pygame.Surface(event.dict['size']).convert_alpha()
                    self.screenWidth = event.dict['size'][0]
                    self.screenHeight = event.dict['size'][0]
                    
                    self.app.updateSize(event.dict['size'])#TODO rewrite so menu is fixed height
                   
                    pygame.display.update()
                    print self.screenWidth,self.screenHeight
                else:
                    # Pass the event off to pgu
                    self.app.event(event)
            # Render the game
            rect = self.app.get_render_area()
            updates = []
            self.display.set_clip(rect)
            lst = self.render(self.display, rect)
            if (lst):
                updates += lst
            self.display.set_clip()

            # Cap it at 30fps
            self.clock.tick(30)

            # Give pgu a chance to update the display
            lst = self.app.update()
            if (lst):
                updates += lst
            pygame.display.update(updates)
            
            pygame.time.wait(10)

