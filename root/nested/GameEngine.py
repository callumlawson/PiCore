'''
Created on 9 Sep 2012

@author: Callum
'''

import random
import math
import pygame
from VirtualCore import VirtualCore
from pgu import gui, timer
from GUI import MainGui
from Parser import Parser

class GameEngine(object):
    
    #Global - I will kill you if you add statics
    padding = 3
    colors = (pygame.Color(255,0,0),pygame.Color(0,255,0),pygame.Color(0,0,255),pygame.Color(0,255,255))
    
    def __init__(self, pygameDisplay):
        
        self.initCoreSize = 3016
        self.programNames = []   
        self.menuHeight = 70
        self.display = pygameDisplay
        self.screenWidth = pygame.display.Info().current_w
        self.screenHeight = pygame.display.Info().current_h
        
        self.drawArea = pygame.Surface((self.screenWidth,self.screenHeight)).convert_alpha()
        self.drawArea.fill((120,120,120)) 
        
        self.app = MainGui(self.display,(self.screenWidth,self.screenHeight),self.menuHeight,self.initCoreSize)
        self.app.engine = self
        
        self.rect = self.app.get_render_area()
        
        self.startGame(self.initCoreSize, [], [])
        
        self.doResize()
        
        self.programNames = []
        self.programPaths = []       
    
    def startGame(self,coreSize,programNames,programPaths):
        self.programNames = programNames
        self.programPaths = programPaths
        programs = []
        parser = Parser()
        for path in self.programPaths:
            programs.append(parser.processFile(path))
        self.virtualCore = VirtualCore(coreSize)
        c = 0
        for program in programs:
            pos = int((c*coreSize)/len(programs) + random.randint(0, int(1.5 * len(program))))
            self.virtualCore.load(pos, program)
            c +=1      
        self.doResize()
    
    # Pause the game clock    
    def pause(self):
        print "pause"
        self.clock.pause()

    # Resume the game clock
    def resume(self):
        print "resume"
        self.clock.resume()
        
    def doResize(self):
        
        self.numberInX = math.ceil(math.sqrt((self.screenWidth * self.virtualCore.size)/(self.screenHeight-self.menuHeight))) #ratio of x rounded up
        self.numberInY = math.ceil(self.virtualCore.size/self.numberInX) # and so in Y
        
        #the 'perfect' size for each cell would be
        xSize = self.screenWidth/self.numberInX
        ySize = (self.screenHeight-self.menuHeight)/self.numberInY
        
        #choose the smaller one to make squares
        if(xSize < ySize):
            self.squareSize = xSize
        else:
            self.squareSize = ySize
        self.fullRender()
        
    def partRender(self):
        for index in self.virtualCore.getChanges():
            y = int(index/self.numberInX)
            x = int(index%self.numberInX)
            pygame.draw.rect(self.drawArea,pygame.Color(0,0,0) ,(x*(self.squareSize), y*(self.squareSize),self.squareSize+self.padding,self.squareSize+self.padding), self.padding/2)
            self.renderRectangle(x, y, index)
        self.virtualCore.clearChanges()
        self.display.blit(self.drawArea,(0,0))
        return (self.rect, )
    
    def fullRender(self): #Do the drawing stuff!
        self.virtualCore.clearChanges()
        pygame.draw.rect(self.drawArea,pygame.Color(0,0,0),(0,0,self.screenWidth,self.screenHeight-self.menuHeight))
       
        count = 0
        for y in xrange(int(self.numberInY)):
            for x in xrange(int(self.numberInX)):
                self.renderRectangle(x, y, count)       
                count +=1
                if(count == self.virtualCore.size):
                    break;
        self.display.blit(self.drawArea,(0,0))
        return (self.rect, )
    
    def renderRectangle(self, x, y, index):
        instruction = self.virtualCore.memory[index]
        if instruction.lastMod == -1:
            pygame.draw.rect(self.drawArea,pygame.Color(200,200,200) ,(self.padding + x*(self.squareSize),self.padding + y*(self.squareSize),self.squareSize-self.padding,self.squareSize-self.padding), 0)
        else:
            pygame.draw.rect(self.drawArea,self.colors[instruction.lastMod] ,(self.padding + x*(self.squareSize),self.padding + y*(self.squareSize),self.squareSize-self.padding,self.squareSize-self.padding), 0)
        for playerCounter in self.virtualCore.playerCounters: #This could be done quicker
            if index in playerCounter.counters:
                pygame.draw.rect(self.drawArea,pygame.Color(255,255,0) ,(x*(self.squareSize), y*(self.squareSize),self.squareSize+self.padding,self.squareSize+self.padding), self.padding/2)
                
    def run(self):
        self.app.update()
        pygame.display.flip()
        self.font = pygame.font.SysFont("", 16)
        self.clock = timer.Clock() #pygame.time.Clock()
        
        # Main program loop
        done = False
        while not done:
            self.rect = self.app.get_render_area()                       
            #Update the game
            if not self.clock.paused and self.virtualCore != None: 
                ret = self.virtualCore.tick()
                if(ret != None): #player out
                    print "Player " + str(ret.playerID) + " who loaded " + self.programNames[ret.playerID] + " lost. There are " + str(ret.playersLeft) + " players remaining"
            # Process events
            for event in pygame.event.get():
                if (event.type == pygame.QUIT or 
                    event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    done = True 
                if event.type == pygame.VIDEORESIZE:
                    self.display = pygame.display.set_mode(event.dict['size'],pygame.RESIZABLE)
                    self.drawArea = pygame.Surface(event.dict['size']).convert_alpha()
                    self.screenWidth = event.dict['size'][0]
                    self.screenHeight = event.dict['size'][1]
                    self.app.updateSize(event.dict['size'])#TODO rewrite so menu is fixed height
                    pygame.display.update()
                    print self.screenWidth,self.screenHeight
                    self.app.event(event)
                    self.doResize()
                else:
                    # Pass the event off to pgu
                    self.app.event(event)
                    
            # Render the game
            updates = []
            self.display.set_clip(self.rect)
            lst = self.partRender()
            if (lst):
                updates += lst
                
            self.display.set_clip()

            # Cap it at 30fps
            #self.clock.tick(20)

            # Give pgu a chance to update the display (menu)
            lst = self.app.update()
            if (lst):
                updates += lst
            pygame.display.update(updates)
            
            pygame.time.wait(30)

