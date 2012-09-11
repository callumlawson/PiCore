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
    def __init__(self, pygameDisplay): #Display passed when game starts
        
        #Parser
        parser = Parser()
        for instruction in  parser.processFile("demoCode.txt"):
            print instruction.printInstruction()
        
        #Render
        self.display = pygameDisplay
        
        self.square = pygame.Surface((200,300)).convert_alpha()
        self.square.fill((0,255,255))
        
        self.application = MainGui(self.display)
        self.application.engine = self

    # Pause the game clock
    def pause(self):
        self.clock.pause()

    # Resume the game clock
    def resume(self):
        self.clock.resume()

    def render(self, dest, rect): #Do the drawing stuff
        
        #Draw a rotating square
        angle = self.clock.get_time()*10
        surf = pygame.transform.rotozoom(self.square, angle, 1)
        r = surf.get_rect()
        r.center = rect.center
        dest.fill((0,0,0), rect)
        self.display.blit(surf, r)

        return (rect,)

    def run(self):
        
        self.application.update()
        pygame.display.flip() #Update full display to screen

        self.font = pygame.font.SysFont("", 16)
        self.clock = timer.Clock() #pygame.time.Clock()
        
        done = False
        while not done:
            # Process events
            for ev in pygame.event.get():
                if (ev.type == pygame.QUIT or 
                    ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE):
                    done = True
                else:
                    # Pass the event off to pgu
                    self.application.event(ev)
                    
            # Render the game
            rect = self.application.get_render_area()
            updates = []
            self.display.set_clip(rect)
            
            renderRectangle = self.render(self.display, rect) #Get the scene
            
            if (renderRectangle):
                updates += renderRectangle
            self.display.set_clip()

            # Cap it at 30fps
            self.clock.tick(30)

            # Give pgu a chance to update the display
            renderRectangle = self.application.update()#Get the menu
            
            if (renderRectangle):
                updates += renderRectangle
                
            pygame.display.update(updates) #Paint the updated regions (given as a list of rectangles)
            
            pygame.time.wait(10)

