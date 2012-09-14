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
from pygame.locals import *


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
        
class ProgramSelector(gui.Dialog):
     
    def __init__(self,**params):
        title = gui.Label("PiCore Program Selector")
        self._count = 1
        self.programNames = []
        self.programPaths = []
        
        def clear_list(arg):
            my_list.clear()
            my_list.resize()
            my_list.repaint()
            self.programNames = []
            self.programPaths = []

        def remove_list_item(arg):
            v = my_list.value
            if v:
                item = v
                print item
                my_list.remove(item)
                my_list.resize()
                my_list.repaint()
                #self.programNames.pop(item-1)
                #self.programPaths.pop(item-1)
                print self.programNames
                print self.programPaths

        def add_list_item(arg):
            my_list.add(arg,value = self._count)
            my_list.resize()
            my_list.repaint()
            self._count += 1
            
        ##Open File Dialog - to load user programs
        def open_file_browser(arg):
            fileDialog = gui.FileDialog()
            fileDialog.connect(gui.CHANGE, handle_file_browser_closed, fileDialog)
            fileDialog.open()
        
        def handle_file_browser_closed(dlg):
            if dlg.value: 
                #input_file.value = dlg.value 
                progName = dlg.input_file.value.split(".")[0]
                add_list_item(progName)
                self.programNames.append(progName)
                self.programPaths.append(dlg.value)
                print self.programNames
                print self.programPaths

        #List selector
        listContainer = gui.Container(width=400, height=150)
        my_list = gui.List(width= 200, height=100)  
        listContainer.add(my_list, 220, 20) 
         
        button = gui.Button("Add program", width=150)
        listContainer.add(button, 20, 30)
        button.connect(gui.CLICK, open_file_browser, None)

        button = gui.Button("remove selected", width=150)
        listContainer.add(button, 20, 60)
        button.connect(gui.CLICK, remove_list_item, None)

        button = gui.Button("clear", width=150)
        listContainer.add(button, 20, 90)
        button.connect(gui.CLICK, clear_list, None)
        
        gui.Dialog.__init__(self,title,listContainer)

class MainGui(gui.Desktop):
    #gameAreaHeight = 550
    menuHeight = 80
    gameArea = None
    menuArea = None
    # The game engine
    engine = None
    display = None
    
    opened = False

    def __init__(self, pygameDisplay, screenSize, menuHeight):
        self.menuHeight = menuHeight
        self.display = pygameDisplay
        gui.Desktop.__init__(self)
        
        self.updateSize(screenSize)
        
    def open(self, dlg, pos=None):
        # Gray out the game area before showing the popup
        if(not self.opened):
            rect = self.gameArea.get_abs_rect()
            dark = pygame.Surface(rect.size).convert_alpha()
            dark.fill((0,0,0,150))
            pygame.display.get_surface().blit(dark, rect)
            # Save whatever has been rendered to the 'game area' so we can
            # render it as a static image while the dialog is open.
            self.gameArea.save_background()
            self.opened = True
            
        # Pause the gameplay while the dialog is visible
        running = not(self.engine.clock.paused)
        self.engine.pause()
        
        size = (self.engine.screenWidth,self.engine.screenHeight)
        pygame.display.set_mode((self.engine.screenWidth,self.engine.screenHeight+1))
        
        gui.Desktop.open(self, dlg, pos)
        while (dlg.is_open()):#
            for event in pygame.event.get():
                self.event(event)
                
            rects = self.update()
            if (rects):
                pygame.display.update(rects)
        if (running):
            # Resume gameplay
            self.opened = False
            pygame.display.set_mode(size,pygame.RESIZABLE)
            self.updateSize(size)
            pygame.display.update()
            self.engine.resume()
        
    def updateSize(self, screenSize):
        self.gameArea = DrawingArea(screenSize[0],screenSize[1]-self.menuHeight)
        self.menuArea = gui.Container(height = self.menuHeight)
        
        table = gui.Table(height = screenSize[1])
        table.tr()
        table.td(self.gameArea)
        table.tr()
        table.td(self.menuArea)

        self.setup_menu()

        self.init(table, self.display)

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
       

        # Add a slider for adjusting the game clock speed
        speedSelTable = gui.Table()

        timeLabel = gui.Label("Tick Speed")

        speedSelTable.tr()
        speedSelTable.td(timeLabel)

        slider = gui.HSlider(value=23,min=0,max=100,size=20,height=16,width=120)

        def update_speed():
            self.engine.clock.set_speed(slider.value/10.0)

        slider.connect(gui.CHANGE, update_speed)

        speedSelTable.tr()
        speedSelTable.td(slider)
        
        #Program selector button
        programSelectorDialog = ProgramSelector()
        loadProgsBtn = gui.Button("Load Programs", height=50)
        loadProgsBtn.connect(gui.CLICK,programSelectorDialog.open,None)
        
        #table.td(loadFileTable)
        table.td(loadProgsBtn)
        table.td(pauseResumeBtn)
        table.td(speedSelTable)
        
        self.menuArea.add(table, 0, 0)
        

    def get_render_area(self):
        return self.gameArea.get_abs_rect()
    
   


