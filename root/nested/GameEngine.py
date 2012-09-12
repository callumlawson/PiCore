'''
Created on 9 Sep 2012

@author: Callum
'''

import pygame
import time
import math
import pgu
from VirtualCore import VirtualCore
from pgu import gui, timer
from GUI import MainGui
from Parser import Parser

class GameEngine(object):
    
    #Global
    screenWidth,screenHeight = 0,0
    memorySize = 10000
    numPlayers = 2
    squareSize = 5
    padding = 3
    menuHeight = 70
    
    display = None
    drawArea = None
    virtualCore = None
    
    def __init__(self, pygameDisplay):
        
        self.display = pygameDisplay
        self.screenWidth = pygame.display.Info().current_w
        self.screenHeight = pygame.display.Info().current_h
        
        #self.virtualCore = VirtualCore(self.memorySize,self.numPlayers)
        
        #Parser
        parser = Parser()
        for instruction in  parser.processFile("demoCode.txt"):
            print instruction.printInstruction()
    
        self.drawArea = pygame.Surface((self.screenWidth,self.screenHeight)).convert_alpha()
        self.drawArea.fill((120,120,120))
        
        self.app = MainGui(self.display,(self.screenWidth,self.screenHeight),self.menuHeight)
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

        pygame.draw.rect(self.drawArea,pygame.Color(0,0,0),(0,0,self.screenWidth,self.screenHeight-self.menuHeight))
        
        #TODO the self.screenHeight is stil wrong because of the menu. But otherwise this works
        
        #I did some maths =p. Lets w is the width of the screen, h the height. X the number in a row, Y the number in a column. N the number of squares
        #We would like the ratio of w:h to be equal to x:y. So (w/h) = (x/y).
        #Lets assume that we end up with roughly a square, so xy = N
        # via substitution we get x = root(wN/h). 
        
        numberInX = math.ceil(math.sqrt((self.screenWidth * self.memorySize)/(self.screenHeight-self.menuHeight))) #ratio of x rounded up
        numberInY = math.ceil(self.memorySize/numberInX) # and so in Y
        
        #the 'perfect' size for each cell would be
        xSize = self.screenWidth/numberInX
        ySize = (self.screenHeight-self.menuHeight)/numberInY
        
        #choose the smaller one to make squares
        if(xSize < ySize):
            self.squareSize = xSize
        else:
            self.squareSize = ySize
                
        count = 0 
        for y in xrange(int(numberInY)):
            for x in xrange(int(numberInX)):
                count+=1
                if(count == self.memorySize):
                    break;
                for counter in self.virtualCore.playerCounters: #This could be done quicker
                    if count == counter:
                        pygame.draw.rect(self.drawArea,pygame.Color(255,255,0) ,(self.padding + x*(self.squareSize),self.padding + y*(self.squareSize),self.squareSize-self.padding,self.squareSize-self.padding), 2)
                instruction = self.virtualCore.memory[count]
                if instruction.name == "nop":
                    pygame.draw.rect(self.drawArea,pygame.Color(200,200,200) ,(self.padding + x*(self.squareSize),self.padding + y*(self.squareSize),self.squareSize-self.padding,self.squareSize-self.padding), 0)
                elif instruction.lastMod != -1:
                    color = pygame.Color((instruction.lastMod%0)*255,(instruction.lastMod%1)*255,(instruction.lastMod%2)*255) #Not efficient or sensible - but a fun idea
                    pygame.draw.rect(self.drawArea,color ,(self.padding + x*(self.squareSize),self.padding + y*(self.squareSize),self.squareSize-self.padding,self.squareSize-self.padding), 0)
                    
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
                    self.screenHeight = event.dict['size'][1]
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
            self.clock.tick(20)

            # Give pgu a chance to update the display
            lst = self.app.update()
            if (lst):
                updates += lst
            pygame.display.update(updates)
            
            pygame.time.wait(10)

