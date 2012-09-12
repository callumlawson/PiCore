'''
Created on 7 Sep 2012

@author: Callum Lawson
'''

import Instruction 
import PlayerProgramCounter
import Parser
import math
from Instruction import Instruction
from PlayerProgramCounter import PlayerProgramCounter
from Parser import Parser

def debugTest():
    myCore = VirtualCore(256,1)
    myParser = Parser()
    aProgram = myParser.processFile("demoCode.txt")
    myCore.load(0, aProgram)
    for i in range(10):
        myCore.tick()
    print "hello"
class PlayerGone:
    playerID = -1
    playersLeft = -1
    def __init__ (self, ID, Left):
        self.playerID = ID
        self.playersLeft = Left
class VirtualCore:
    
    playerCounters = []
    currentPlayer = 0
    memory = []
    size = 0
    changesList = []
    
    def __init__(self, memorySize, players):
        self.playerCounters = [PlayerProgramCounter(i) for i in range(players)]
        self.memory = [Instruction() for j in range(memorySize)]
        self.size = memorySize
        
    def load(self, position, code):
        codeLength = len(code)
        self.memory = self.memory[0:position] + code + self.memory[(position + codeLength):]
    def getChanges(self):
        print "Im a blue monkey"
        return self.changesList
    def clearChanges(self):
        changesList = []    
    def tick(self): #will return a PlayerGone object if a player loses. None otherwise.
        self.setROM()
        nextInstructionLocation = self.playerCounters[self.currentPlayer].currentPointer()
        nextInstruction = self.memory[nextInstructionLocation]
        if(self.execute(nextInstruction, nextInstructionLocation)):
            remain = len(self.playerCounters) - 1
            returnObject = PlayerGone(self.playerCounters.pop(self.currentPlayer).ID,remain)
            self.currentPlayer %= remain
            return returnObject
        else:
            self.currentPlayer = (self.currentPlayer + 1)%len(self.playerCounters)
        return None
        
    def execute(self, instruction, instructionLocation):   #will return true if the player has lost his last thread
        #TODO: execute instructions. Should edit self.memory and call advancePointer and/or advanceThread if relevant
        instruction.lastMod = self.currentPlayer
        self.changesList.append(instructionLocation)
        if(instruction.name == "nop"): #do nothing. Duh
            self.playerCounters[self.currentPlayer].advanceBoth(self.size)
            
        elif(instruction.name == "dat"): #Just. Die.
            return self.playerCounters[self.currentPlayer].killCurrentPointer()
        
        elif(instruction.name == "mov"): # move
            thingToMove = self.getInstruction(instruction.arguments[0], instructionLocation)
            location = self.getLocation(instruction.arguments[1], instructionLocation)
            if(location == -1): #invalid destination, kills thread
                return self.playerCounters[self.currentPlayer].killCurrentPointer()
            thingToMove.lastMod = self.currentPlayer
            location.lastMod = self.currentPlayer
            self.memory[location] = thingToMove
            self.playerCounters[self.currentPlayer].advanceBoth(self.size)
            
        elif(instruction.name == "jmp"): #jump program counter to a point in memory
            destination = self.getLocation(instruction.arguments[0], instructionLocation)
            if(destination == -1):
                return self.playerCounters[self.currentPlayer].killCurrentPointer()
            destination.lastMod = self.currentPlayer
            self.playerCounters[self.currentPlayer].jumpPointer(destination)
            self.playerCounters[self.currentPlayer].advanceThread()
            
        elif(instruction.name == "add"): # add
            return self.mathOperation(instruction, instructionLocation, self.addOperation) 
            
        elif(instruction.name == "sub"): # add
            return self.mathOperation(instruction, instructionLocation, self.subOperation) 
            
        elif(instruction.name == "mlt"): # add
            return self.mathOperation(instruction, instructionLocation, self.multOperation) 
            
        elif(instruction.name == "dvd"): # add
            return self.mathOperation(instruction, instructionLocation, self.divOperation) 
            
        elif(instruction.name == "jpi"): #jump if
            firstargument = self.getInstruction(instruction.arguments[1],instructionLocation)
            secondargument = self.getInstruction(instruction.arguments[2],instructionLocation)
            firstargument.lastMod = self.currentPlayer
            secondargument.lastMod= self.currentPlayer
            
            if(firstargument.arguments[0][1] == secondargument[0][1]):
                destination = self.getLocation(instruction.arguments[0], instructionLocation)
                if(destination == -1):
                    return self.playerCounters[self.currentPlayer].killCurrentPointer()
                destination.lastMod = self.currentPlayer
                self.playerCounters[self.currentPlayer].jumpPointer(destination)
                self.playerCounters[self.currentPlayer].advanceThread()
            else:
                self.playerCounters[self.currentPlayer].advanceBoth(self.size)
                
        elif(instruction.name == "bch"): # new thread?
            destination = self.getLocation(instruction.arguments[0], instructionLocation)
            if(destination == -1):
                    return self.playerCounters[self.currentPlayer].killCurrentPointer()
            destination.lastMod = self.currentPlayer
            self.playerCounters[self.currentPlayer].advancePointer()
            self.playerCounters[self.currentPlayer].spawnThead(destination)
            self.playerCounters[self.currentPlayer].advanceThread()
            
        return False
    
    def mathOperation(self, instruction, instructionLocation, op):
        firstargument = self.getInstruction(instruction.arguments[0],instructionLocation)
        secondargument = self.getInstruction(instruction.arguments[1],instructionLocation)
        location = self.getLocation(instruction.arguments[2],instructionLocation)
        if(location == -1): #invalid destination, kills thread
            return self.playerCounters[self.currentPlayer].killCurrentPointer()
        firstargument.lastMod = self.currentPlayer
        secondargument.lastMod = self.currentPlayer
        self.memory[location].argument[0] = (self.memory[location].arguments[0][0],op(firstargument.arguments[0][1] , secondargument.arguments[0][1])%self.size)
        self.playerCounters[self.currentPlayer].advanceBoth(self.size)
        return False
    
    def addOperation(self, op1, op2):
        return op1 + op2
    def subOperation(self, op1, op2):
        return op1 - op2
    def multOperation(self, op1, op2):
        return op1 * op2
    def divOperation(self, op1, op2):
        return math.floor(op1 / op2)
    
    def getInstruction(self, argumentTuple, relativePoint): #returns the instruction in the relevent location (or makes the pseudo data for literals)
        atLocation = self.getLocation(argumentTuple, relativePoint)
        if(atLocation == -1):
            return Instruction("dat", [argumentTuple])
        elif(argumentTuple[0] == "$"):
            #TODO: stuff concerning read only stuff
            pass
        return self.memory[atLocation]
            
    def getLocation(self, argumentTuple, relativePoint): #return -1 if not valid
        loc = -1
        if(argumentTuple[0] == ""):
            return -1
        elif(argumentTuple[0] == "@"):
            loc = (argumentTuple[1] + relativePoint)%self.size
        elif(argumentTuple[0] == "#"):
            loc = (self.memory[(argumentTuple[1] + relativePoint)%self.size].arguments[0][1] + relativePoint)%self.size
        elif(argumentTuple[0] == "$"):
            #TODO: stuff concerning read only stuff
            pass
        self.changesList.append(loc)
        return loc
    def setROM(self):
        #TODO: set the read only memory
        pass



