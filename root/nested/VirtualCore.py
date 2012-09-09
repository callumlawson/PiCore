'''
Created on 7 Sep 2012

@author: Callum
'''

import Instruction 
import PlayerProgramCounter
import math
from Instruction import Instruction
from PlayerProgramCounter import PlayerProgramCounter
 
class VirtualCore:
    
    playerCounters = []
    currentPlayer = 0
    memory = []
    size = 0
    
    def __init__(self, memorySize, players):
        self.playerCounters = [PlayerProgramCounter(i) for i in range(players)]
        self.memory = [Instruction() for j in range(memorySize)]
        self.size = memorySize
        
    def load(self, position, code):
        codeLength = len(code)
        self.memory = self.memory[0:position] + code + self.memory[(position + codeLength):]
        
    def tick(self): #will return true if only one player remains
        self.setROM()
        nextInstructionLocation = self.playerCounters[self.currentPlayer].currentPointer()
        nextInstruction = self.memory[nextInstructionLocation]
        if(self.execute(nextInstruction, nextInstructionLocation)):
            #TODO: feed out that a player has lost even if the game is not over (relevant for more than two players)
            self.playerCounters.pop(self.currentPlayer)
            remain = len(self.playerCounters)
            if(remain == 1):
                return True
            self.currentPlayer %= remain
        else:
            self.currentPlayer = (self.currentPlayer + 1)%len(self.playerCounters)
        return False
        
    def execute(self, instruction, instructionLocation):   #will return true if the player has lost his last thread
        #TODO: execute instructions. Should edit self.memory and call advancePointer and/or advanceThread if relevant
        if(instruction.name == "nop"): #do nothing. Duh
            self.playerCounters[self.currentPlayer].advanceBoth(self.size)
            
        elif(instruction.name == "dat"): #Just. Die.
            return self.playerCounters[self.currentPlayer].killCurrentPointer()
        
        elif(instruction.name == "mov"): # move
            instruction = self.getInstruction(instruction.arguments[0], instructionLocation)
            location = self.getLocation(instruction.arguments[1], instructionLocation)
            if(location == -1): #invalid destination, kills thread
                return self.playerCounters[self.currentPlayer].killCurrentPointer()
            self.memory[location] = instruction
            self.playerCounters[self.currentPlayer].advanceBoth(self.size)
            
        elif(instruction.name == "jmp"): #jump program counter to a point in memory
            destination = self.getLocation(instruction.arguments[0], instructionLocation)
            if(destination == -1):
                return self.playerCounters[self.currentPlayer].killCurrentPointer()
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
            if(firstargument.arguments[0][1] == secondargument[0][1]):
                destination = self.getLocation(instruction.arguments[0], instructionLocation)
                if(destination == -1):
                    return self.playerCounters[self.currentPlayer].killCurrentPointer()
                self.playerCounters[self.currentPlayer].jumpPointer(destination)
                self.playerCounters[self.currentPlayer].advanceThread()
            else:
                self.playerCounters[self.currentPlayer].advanceBoth(self.size)
                
        elif(instruction.name == "bch"): # new thread?
            destination = self.getLocation(instruction.arguments[0], instructionLocation)
            if(destination == -1):
                    return self.playerCounters[self.currentPlayer].killCurrentPointer()
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
        if(argumentTuple[0] == ""):
            return Instruction("dat", [argumentTuple])
        elif(argumentTuple[0] == "@"):
            return self.memory[(argumentTuple[1] + relativePoint)%self.size]
        elif(argumentTuple[0] == "#"):
            return self.memory[(self.memory[(argumentTuple[1] + relativePoint)%self.size].arguments[0][1] + relativePoint)%self.size]
        elif(argumentTuple[0] == "$"):
            #TODO: stuff concerning read only stuff
            foo = 1
            
    def getLocation(self, argumentTuple, relativePoint): #return -1 if not valid
        if(argumentTuple[0] == ""):
            return -1
        elif(argumentTuple[0] == "@"):
            return (argumentTuple[1] + relativePoint)%self.size
        elif(argumentTuple[0] == "#"):
            return (self.memory[(argumentTuple[1] + relativePoint)%self.size].arguments[0][1] + relativePoint)%self.size
        elif(argumentTuple[0] == "$"):
            #TODO: stuff concerning read only stuff
            foo = 1
            
    def setROM(self):
        #TODO: set the read only memory
        foo = 1    