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

    def setup_menu(self): #Init the game menu
        table = gui.Table(vpadding=5, hpadding=2)
        table.tr()
       
        # Add a button for pausing / resuming the game clock
        def pause_cb():
            if (self.engine.clock.paused):
                self.engine.resume()
            else:
                self.engine.pause()

        pauseResumeBtn = gui.Button("Pause/Resume Processor Clock", height=50)
        pauseResumeBtn.connect(gui.CLICK, pause_cb)
        table.td(pauseResumeBtn)

        # Add a slider for adjusting the game clock speed
        table2 = gui.Table()

        timeLabel = gui.Label("Tick Speed")

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

    def get_render_area(self):
        return self.gameArea.get_abs_rect()



