'''
Created on 7 Sep 2012

@author: Callum
'''

import Instruction
import PlayerProgramCounter
import math
 
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
        elif(instruction.name == "data"): #Just. Die.
            return self.playerCounters[self.currentPlayer].killCurrentPointer()
        elif(instruction.name == "mov"): # move
            instruction = self.getInstruction(instruction.values[0], instructionLocation)
            location = self.getLocation(instruction.values[1], instructionLocation)
            if(location == -1): #invalid destination, kills thread
                return self.playerCounters[self.currentPlayer].killCurrentPointer()
            self.memory[location] = instruction
            self.playerCounters[self.currentPlayer].advanceBoth(self.size)
        elif(instruction.name == "jmp"): #jump program counter to a point in memory
            destination = self.getLocation(instruction.values[0], instructionLocation)
            if(destination == -1):
                return self.playerCounters[self.currentPlayer].killCurrentPointer()
            self.playerCounters[self.currentPlayer].jumpPointer(destination)
            self.playerCounters[self.currentPlayer].advanceThread()
        elif(instruction.name == "add"): # add
            firstValue = self.getInstruction(instruction.values[0],instructionLocation)
            secondValue = self.getInstruction(instruction.values[1],instructionLocation)
            location = self.getLocation(instruction.values[2],instructionLocation)
            if(location == -1): #invalid destination, kills thread
                return self.playerCounters[self.currentPlayer].killCurrentPointer()
            self.memory[location] = Instruction("dat",["",(firstValue.values[0][1] + secondValue.values[0][1])%self.size])
            self.playerCounters[self.currentPlayer].advanceBoth(self.size)
        elif(instruction.name == "sub"): # add
            firstValue = self.getInstruction(instruction.values[0],instructionLocation)
            secondValue = self.getInstruction(instruction.values[1],instructionLocation)
            location = self.getLocation(instruction.values[2],instructionLocation)
            if(location == -1): #invalid destination, kills thread
                return self.playerCounters[self.currentPlayer].killCurrentPointer()
            self.memory[location] = Instruction("dat",["",(firstValue.values[0][1] - secondValue.values[0][1])%self.size])
            self.playerCounters[self.currentPlayer].advanceBoth(self.size)
        elif(instruction.name == "jpi"):
            firstValue = self.getInstruction(instruction.values[1],instructionLocation)
            secondValue = self.getInstruction(instruction.values[2],instructionLocation)
            if(firstValue.values[0][1] == secondValue[0][1]):
                destination = self.getLocation(instruction.values[0], instructionLocation)
                if(destination == -1):
                    return self.playerCounters[self.currentPlayer].killCurrentPointer()
                self.playerCounters[self.currentPlayer].jumpPointer(destination)
                self.playerCounters[self.currentPlayer].advanceThread()
            else:
                self.playerCounters[self.currentPlayer].advanceBoth(self.size)
        elif(instruction.name == "bch"):
            destination = self.getLocation(instruction.values[0], instructionLocation)
            if(destination == -1):
                    return self.playerCounters[self.currentPlayer].killCurrentPointer()
            self.playerCounters[self.currentPlayer].advancePointer()
            self.playerCounters[self.currentPlayer].spawnThead(destination)
            self.playerCounters[self.currentPlayer].advanceThread()
        elif(instruction.name == "mlt"): # add
            firstValue = self.getInstruction(instruction.values[0],instructionLocation)
            secondValue = self.getInstruction(instruction.values[1],instructionLocation)
            location = self.getLocation(instruction.values[2],instructionLocation)
            if(location == -1): #invalid destination, kills thread
                return self.playerCounters[self.currentPlayer].killCurrentPointer()
            self.memory[location] = Instruction("dat",["",(firstValue.values[0][1] * secondValue.values[0][1])%self.size])
            self.playerCounters[self.currentPlayer].advanceBoth(self.size)
        elif(instruction.name == "dvd"): # add
            firstValue = self.getInstruction(instruction.values[0],instructionLocation)
            secondValue = self.getInstruction(instruction.values[1],instructionLocation)
            location = self.getLocation(instruction.values[2],instructionLocation)
            if(location == -1): #invalid destination, kills thread
                return self.playerCounters[self.currentPlayer].killCurrentPointer()
            self.memory[location] = Instruction("dat",["",math.floor(firstValue.values[0][1] / secondValue.values[0][1])%self.size])
            self.playerCounters[self.currentPlayer].advanceBoth(self.size)
        return False
    
    def getInstruction(self, valueTuple, relativePoint): #returns the instruction in the relevent location (or makes the pseudo data for literals)
        if(valueTuple[0] == ""):
            return Instruction("dat", [valueTuple])
        elif(valueTuple[0] == "@"):
            return self.memory[(valueTuple[1] + relativePoint)%self.size]
        elif(valueTuple[0] == "#"):
            return self.memory[(self.memory[(valueTuple[1] + relativePoint)%self.size].values[0][1] + relativePoint)%self.size]
        elif(valueTuple[0] == "$"):
            #TODO: stuff concerning read only stuff
            foo = 1
            
    def getLocation(self, valueTuple, relativePoint): #return -1 if not valid
        if(valueTuple[0] == ""):
            return -1
        elif(valueTuple[0] == "@"):
            return (valueTuple[1] + relativePoint)%self.size
        elif(valueTuple[0] == "#"):
            return (self.memory[(valueTuple[1] + relativePoint)%self.size].values[0][1] + relativePoint)%self.size
        elif(valueTuple[0] == "$"):
            #TODO: stuff concerning read only stuff
            foo = 1
            
    def setROM(self):
        #TODO: set the read only memory
        foo = 1    