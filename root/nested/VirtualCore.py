'''
Created on 7 Sep 2012

@author: Callum Lawson
'''
import math
from Instruction import Instruction
from PlayerProgramCounter import PlayerProgramCounter
    
class PlayerGone:
    def __init__ (self, ID, Left):
        self.playerID = ID
        self.playersLeft = Left
        
class VirtualCore:
    # ROM = [memSize,processes,threads,clockCount]
    def __init__(self, memorySize):
        self.playerCounters = []
        self.IDcount = 0
        self.memory = [Instruction() for j in range(memorySize)]
        self.size = memorySize
        self.currentPlayer = 0
        self.ROM = [memorySize-1,0,0,0]
        self.changesList = []
    def load(self, position, code):
        codeLength = len(code)
        self.memory = self.memory[0:position] + code + self.memory[(position + codeLength):]
        self.playerCounters.append(PlayerProgramCounter(self, self.IDcount,position))
        self.IDcount +=1
    def modValues(self):
        for instruc in self.memory:
            for arg in instruc.arguments:
                arg[1] = (arg[0],arg[1]%self.size)
    def getChanges(self):
        #print "Im a blue monkey"
        return self.changesList
    def clearChanges(self):
        self.changesList = []  
          
    def tick(self): #will return a PlayerGone object if a player loses. None otherwise.
        if(len(self.playerCounters) == 0):
            return None
        self.setROM()
        nextInstructionLocation = self.playerCounters[self.currentPlayer].currentPointer()
        nextInstruction = self.memory[nextInstructionLocation]
        if(self.execute(nextInstruction, nextInstructionLocation)):
            remain = len(self.playerCounters) - 1
            returnObject = PlayerGone(self.playerCounters.pop(self.currentPlayer).ID,remain)
            if(remain != 0):
                self.currentPlayer %= remain
            return returnObject
        else:
            self.currentPlayer = (self.currentPlayer + 1)%len(self.playerCounters)
        
        return None
        
    def execute(self, instruction, instructionLocation):   #will return true if the player has lost his last thread
        instruction.lastMod = self.playerCounters[self.currentPlayer].ID
        self.changesList.append(instructionLocation)
        if(instruction.name == "nop"): #do nothing. Duh
            self.playerCounters[self.currentPlayer].advanceBoth()
            
        elif(instruction.name == "dat"): #Just. Die.
            return self.playerCounters[self.currentPlayer].killCurrentPointer()
        
        elif(instruction.name == "mov"): # move
            thingToMove = self.getInstruction(instruction.arguments[0], instructionLocation)
            location = self.getLocation(instruction.arguments[1], instructionLocation)
            if(location == -1): #invalid destination, kills thread
                return self.playerCounters[self.currentPlayer].killCurrentPointer()
            self.memory[location] = thingToMove.clone()
            self.memory[location].lastMod = self.playerCounters[self.currentPlayer].ID
            self.playerCounters[self.currentPlayer].advanceBoth()
            
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
        
        elif(instruction.name == "mod"): # add
            return self.mathOperation(instruction, instructionLocation, self.modOperation) 
        
        elif(instruction.name == "and"): # add
            return self.mathOperation(instruction, instructionLocation, self.andOperation) 
        
        elif(instruction.name == "or"): # add
            return self.mathOperation(instruction, instructionLocation, self.orOperation) 
        
        elif(instruction.name == "xor"): # add
            return self.mathOperation(instruction, instructionLocation, self.xorOperation) 
        
        elif(instruction.name == "nnd"): # add
            return self.mathOperation(instruction, instructionLocation, self.nandOperation) 
      
        elif(instruction.name == "jpi"): #jump if
            firstargument = self.getInstruction(instruction.arguments[1],instructionLocation)
            secondargument = self.getInstruction(instruction.arguments[2],instructionLocation)
            
            if(firstargument.arguments[0][1] == secondargument.arguments[0][1]):
                destination = self.getLocation(instruction.arguments[0], instructionLocation)
                if(destination == -1):
                    return self.playerCounters[self.currentPlayer].killCurrentPointer()
                self.playerCounters[self.currentPlayer].jumpPointer(destination)
                self.playerCounters[self.currentPlayer].advanceThread()
            else:
                self.playerCounters[self.currentPlayer].advanceBoth()
                
        elif(instruction.name == "bch"): # new thread?
            destination = self.getLocation(instruction.arguments[0], instructionLocation)
            if(destination == -1):
                    return self.playerCounters[self.currentPlayer].killCurrentPointer()
            self.playerCounters[self.currentPlayer].advancePointer()
            self.playerCounters[self.currentPlayer].spawnThread(destination)
            self.playerCounters[self.currentPlayer].advanceThread()
            
        return False
    
    def mathOperation(self, instruction, instructionLocation, op):
        firstargument = self.getInstruction(instruction.arguments[0],instructionLocation)
        secondargument = self.getInstruction(instruction.arguments[1],instructionLocation)
        location = self.getLocation(instruction.arguments[2],instructionLocation)
        if(location == -1): #invalid destination, kills thread
            return self.playerCounters[self.currentPlayer].killCurrentPointer()
        self.memory[location].arguments[0] = (self.memory[location].arguments[0][0],op(int(firstargument.arguments[0][1]) , int(secondargument.arguments[0][1]))%self.size)
        self.playerCounters[self.currentPlayer].advanceBoth()
        return False
    
    def addOperation(self, op1, op2):
        return op1 + op2
    def subOperation(self, op1, op2):
        return op1 - op2
    def multOperation(self, op1, op2):
        return op1 * op2
    def divOperation(self, op1, op2):
        return math.floor(op1 / op2)
    def modOperation(self, op1, op2):
        return op1%op2
    def andOperation(self, op1, op2):
        return self.boolToInt((op1 != 0) and (op2 != 0))
    def orOperation(self, op1, op2):
        return self.boolToInt((op1 != 0) or (op2 != 0))
    def xorOperation(self, op1, op2):
        return self.boolToInt((op1 != 0) != (op2 != 0))
    def nandOperation(self, op1, op2):
        return self.boolToInt((op1 == 0) and (op2 == 0))
    def getInstruction(self, argumentTuple, relativePoint): #returns the instruction in the relevent location (or makes the pseudo data for literals)
        if(argumentTuple[0] == "$"):
            return Instruction("dat", argumentTuple[1]%len(self.ROM))
        atLocation = self.getLocation(argumentTuple, relativePoint)
        if(atLocation == -1):
            return Instruction("dat", [argumentTuple])
        return self.memory[atLocation]
    def boolToInt(self, aBool):
        if(aBool):
            return 1
        return 0        
    def getLocation(self, argumentTuple, relativePoint): #return -1 if not valid
        loc = -1
        if(argumentTuple[0] == ""):
            return -1
        elif(argumentTuple[0] == "@"):
            loc = (int(argumentTuple[1]) + relativePoint)%self.size
        elif(argumentTuple[0] == "#"):
            loc = (int(self.memory[(int(argumentTuple[1]) + relativePoint)%self.size].arguments[0][1]) + relativePoint)%self.size
        elif(argumentTuple[0] == "$"):
            return -1
        self.memory[loc].lastMod = self.playerCounters[self.currentPlayer].ID
        self.changesList.append(loc)
        return loc
    def setROM(self):
        self.ROM[3] +=1



