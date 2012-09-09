'''
Created on 9 Sep 2012

@author: Callum
'''

#!/usr/bin/env python

# self is not needed if you have PGU installed
import sys
sys.path.insert(0, "..")

import math
import time
import pygame
import pgu
from pgu import gui, timer



class DrawingArea(gui.Widget): #render the gameState
    def __init__(self, width, height):
        gui.Widget.__init__(self, width=width, height=height)
        self.imageBuffer = pygame.Surface((width, height))

    def paint(self, surf):
        # Paint whatever has been captured in the buffer
        surf.blit(self.imageBuffer, (0, 0))

    # Call self function to take a snapshot of whatever has been rendered
    # onto the display over self widget.
    def save_background(self):
        pygameDisplay = pygame.display.get_surface()
        self.imageBuffer.blit(pygameDisplay, self.get_abs_rect())

class MainGui(gui.Desktop):
    gameAreaHeight = 520
    gameArea = None
    menuArea = None
    # The game engine
    engine = None

    def __init__(self, pygameDisplay):
        gui.Desktop.__init__(self)

        # Setup the 'game' area where the action takes place
        self.gameArea = DrawingArea(pygameDisplay.get_width(),
                                    self.gameAreaHeight)
        # Setup the gui area
        self.menuArea = gui.Container(
            height=pygameDisplay.get_height()-self.gameAreaHeight)

        table = gui.Table(height=pygameDisplay.get_height())
        table.tr()
        table.td(self.gameArea)
        table.tr()
        table.td(self.menuArea)

        self.setup_menu()

        self.init(table, pygameDisplay)

    def setup_menu(self):
        table = gui.Table(vpadding=5, hpadding=2)
        table.tr()
       
        # Add a button for pausing / resuming the game clock
        def pause_cb():
            if (self.engine.clock.paused):
                self.engine.resume()
            else:
                self.engine.pause()

        pauseResumeBtn = gui.Button("Pause/resume clock", height=50)
        pauseResumeBtn.connect(gui.CLICK, pause_cb)
        table.td(pauseResumeBtn)

        # Add a slider for adjusting the game clock speed
        table2 = gui.Table()

        timeLabel = gui.Label("Clock speed")

        table2.tr()
        table2.td(timeLabel)

        slider = gui.HSlider(value=23,min=0,max=100,size=20,height=16,width=120)

        def update_speed():
            self.engine.clock.set_speed(slider.value/10.0)

        slider.connect(gui.CHANGE, update_speed)

        table2.tr()
        table2.td(slider)

        table.td(table2)

        self.menuArea.add(table, 0, 0)

    def open(self, dlg, pos=None):
        # Gray out the game area before showing the popup
        rect = self.gameArea.get_abs_rect()
        dark = pygame.Surface(rect.size).convert_alpha()
        dark.fill((0,0,0,150))
        pygame.display.get_surface().blit(dark, rect)
        # Save whatever has been rendered to the 'game area' so we can
        # render it as a static image while the dialog is open.
        self.gameArea.save_background()
        # Pause the gameplay while the dialog is visible
        running = not(self.engine.clock.paused)
        self.engine.pause()
        gui.Desktop.open(self, dlg, pos)
        while (dlg.is_open()):
            for ev in pygame.event.get():
                self.event(ev)
            rects = self.update()
            if (rects):
                pygame.display.update(rects)
        if (running):
            # Resume gameplay
            self.engine.resume()

    def get_render_area(self):
        return self.gameArea.get_abs_rect()


class GameEngine(object):
    def __init__(self, pygameDisplay):
        
        self.disp = pygameDisplay
        self.square = pygame.Surface((400,400)).convert_alpha()
        self.square.fill((0,255,0))
        self.app = MainGui(self.disp)
        self.app.engine = self

    # Pause the game clock
    def pause(self):
        self.clock.pause()

    # Resume the game clock
    def resume(self):
        self.clock.resume()

    def render(self, dest, rect):
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

### Start!
pygameDisplay = pygame.display.set_mode((800, 600)) #Set screen size
engine = GameEngine(pygameDisplay) #Create engine
engine.run() #Get going....

