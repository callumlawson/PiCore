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
    def __init__(self, pygameDisplay):
        
        self.disp = pygameDisplay
        self.square = pygame.Surface((400,400)).convert_alpha()
        self.square.fill((0,255,0))
        self.app = MainGui(self.disp)
        self.app.engine = self
        
            #Parser
        parser = Parser()
        for instruction in  parser.processFile("demoCode.txt"):
            print instruction.printInstruction()

    # Pause the game clock
    def pause(self):
        self.clock.pause()

    # Resume the game clock
    def resume(self):
        self.clock.resume()

    def render(self, dest, rect): #Do the drawing stuff!
        # Draw a rotating square
        angle = self.clock.get_time()*10
        surf = pygame.transform.rotozoom(self.square, angle, 1)
        r = surf.get_rect()
        r.center = rect.center
        dest.fill((0,0,0), rect)
        self.disp.blit(surf, r)

        return (rect,)

    def run(self):
        self.app.update()
        pygame.display.flip()

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
                    self.app.event(ev)
            # Render the game
            rect = self.app.get_render_area()
            updates = []
            self.disp.set_clip(rect)
            lst = self.render(self.disp, rect)
            if (lst):
                updates += lst
            self.disp.set_clip()

            # Cap it at 30fps
            self.clock.tick(30)

            # Give pgu a chance to update the display
            lst = self.app.update()
            if (lst):
                updates += lst
            pygame.display.update(updates)
            
            pygame.time.wait(10)

