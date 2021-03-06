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
        
class AboutDialog(gui.Dialog):
    
    def __init__(self,**params):
        title = gui.Label("About PiCore")
        
        width = 400
        height = 200
        doc = gui.Document(width=width)
        
        space = title.style.font.size(" ")
        
        doc.block(align=0)
        for word in """PiCore v0.8 by Callum Lawson and Lawrence Esswood""".split(" "): 
            doc.add(gui.Label(word))
            doc.space(space)
        doc.br(space[1])
        
        doc.block(align=0)
        for word in """A reincarnation of Corewars for the Raspberry Pi and other platforms.""".split(" "): 
            doc.add(gui.Label(word))
            doc.space(space)
        doc.br(space[1])
        
        gui.Dialog.__init__(self,title,doc)
##
        
class ErrorDialog(gui.Dialog):
    
    def __init__(self,errorMessages):
        font = pygame.font.SysFont("", 22)
        title = gui.Label("Error")
        title.set_font(font)
    
        container = gui.Container(width=400,height =180)
        
        doc = gui.Document(width=380)
        space = title.style.font.size(" ")
        
        doc.block(align=-1)
        
        for message in errorMessages:
            messageLabel = gui.Label(message)
            messageLabel.set_font(font)
            doc.add(messageLabel)
            doc.br(space[1])
            
        container.add(gui.ScrollArea(doc,390,160),5,10)
        
        gui.Dialog.__init__(self,title,container)
        
class ProgramSelector(gui.Dialog):
     
    def __init__(self,MainGui):
        title = gui.Label("PiCore Program Selector")
        self.programNames = []
        self.programPaths = []
        self.mainGui = MainGui
        
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
                
                for i in my_list.items:
                    if i.value == item: theItem = i
                
                my_list.remove(item)
                my_list.resize()
                my_list.repaint()
                
                self.programNames.remove(theItem.widget.value)
                self.programPaths.remove(item)

        def add_list_item(arg,path):
            my_list.add(arg,value = path)
            self.programNames.append(arg)
            self.programPaths.append(path)
            my_list.resize()
            my_list.repaint()
           
        ##Open File Dialog - to load user programs
        def open_file_browser(arg):
            fileDialog = gui.FileDialog()
            fileDialog.connect(gui.CHANGE, handle_file_browser_closed, fileDialog)
            fileDialog.open()
        
        def handle_file_browser_closed(dlg):
            if dlg.value: 
                #input_file.value = dlg.value 
                progName = dlg.input_file.value.split(".")[0]
                
                if not progName == "":
                    add_list_item(progName,dlg.value)              

        def handle_submit(arg):
            print "Submit button pressed"
            self.mainGui.programNames = self.programNames
            self.mainGui.programPaths = self.programPaths
            #self.mainGui.engine.
            self.close(self)
        
        #List selector
        listContainer = gui.Container(width=400, height=150)
        my_list = gui.List(width= 210, height=125)  
        listContainer.add(my_list, 185, 10) 
         
        button = gui.Button("Add program", width=150)
        listContainer.add(button, 10, 20)
        button.connect(gui.CLICK, open_file_browser, None)

        button = gui.Button("Remove selected", width=150)
        listContainer.add(button, 10, 50)
        button.connect(gui.CLICK, remove_list_item, None)

        button = gui.Button("Clear", width=150)
        listContainer.add(button, 10, 80)
        button.connect(gui.CLICK, clear_list, None)
        
        button = gui.Button("Load", width=150)
        listContainer.add(button, 10, 110)
        button.connect(gui.CLICK, handle_submit , None)
        
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

    def __init__(self, pygameDisplay, screenSize, menuHeight,initCoreSize):
        self.sliderValue = 25
        self.menuHeight = menuHeight
        self.display = pygameDisplay
        gui.Desktop.__init__(self)
        self.coreSize = initCoreSize
        self.programNames = []
        self.programPaths = []
        self.updateSize(screenSize)#Also sets up menu
        
        
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
        def pause():
            if (self.engine.clock.paused):
                self.engine.resume()
                pauseResumeBtn.value = "Pause"
            else:
                self.engine.pause()
                pauseResumeBtn.value = "Resume"

        pauseResumeBtn = gui.Button("Pause", height=50)
        pauseResumeBtn.connect(gui.CLICK, pause)
       
        # Add a slider for adjusting the game clock speed
        speedSelTable = gui.Table()

        timeLabel = gui.Label("Tick Speed")
        
        speedSelTable.tr()
        speedSelTable.td(timeLabel)

        def update_speed():
            self.sliderValue = slider.value
            if slider.value != 100:
                self.engine.clock.set_speed(self.sliderValue/10.0)
            else: self.engine.clock.set_speed(10000)
            
        def update_core_size():
            self.coreSize = int(coreSizeInput.value)
            
        def update_tick_limit():
            self.tickLimit = int(tickLimitInput.value)
        
        def start_test(arg):
            self.engine.testTwo(self.programNames,self.programPaths)
        
        coreSizeLabel = gui.Label("Core Size:")
        coreSizeInput = gui.Input(value = 3000 ,size = 5)
        
        tickLimitLabel = gui.Label("Tick Limit:")
        tickLimitInput = gui.Input(value = 10000, size = 5)
        
        slider = gui.HSlider(value=self.sliderValue,min=0,max=100,size=20,height=16,width=120)
        slider.connect(gui.CHANGE, update_speed)

        speedSelTable.tr()
        speedSelTable.td(slider)
        
        #Program selector button
        aboutDialog = AboutDialog()
        programSelectorDialog = ProgramSelector(self)
      
        loadProgsBtn = gui.Button("Load Programs", height=50)
        loadProgsBtn.connect(gui.CLICK,programSelectorDialog.open,None)
        
        testProgsBtn = gui.Button("Test Programs", height=50)
        testProgsBtn.connect(gui.CLICK,start_test,None)
        
        aboutBtn = gui.Button("About",height=50)
        aboutBtn.connect(gui.CLICK,aboutDialog.open,None)
        
        def start_sim(arg):
            update_core_size()
            update_tick_limit()
            self.engine.startGame(self.coreSize,self.programNames,self.programPaths,self.tickLimit)
            
        startBtn = gui.Button("Start", height=50)
        startBtn.connect(gui.CLICK,start_sim,None)
        
        settingsTable = gui.Table()
        
        table.td(startBtn, height=50)
       
        table.td(pauseResumeBtn)
        table.td(speedSelTable)
        
        settingsTable.td(coreSizeLabel,col = 0, row = 0)
        settingsTable.td(coreSizeInput,col = 1, row = 0)
    
        settingsTable.td(tickLimitLabel,col = 0, row = 1)
        settingsTable.td(tickLimitInput,col = 1, row = 1)
        
        table.td(settingsTable)
        
        table.td(loadProgsBtn)
        
        table.td(testProgsBtn)
        
        table.td(aboutBtn)
        
        self.menuArea.add(table, 0, 0)
        
    def open_error_dialog(self,messages):
            errorDialog = ErrorDialog(messages)
            errorDialog.open() 
        
    def get_render_area(self):
        return self.gameArea.get_abs_rect()
    
   


