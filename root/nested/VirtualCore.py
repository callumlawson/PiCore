'''
Created on 7 Sep 2012

@author: Callum
'''

import Instruction
import PlayerProgramCounter
 
class VirtualCore:
    playerCounters = []
    currentPlayer = 0
    memmory = []
    size = 0
    def __init__(self, memmorySize, players):
        self.playerCounters = [PlayerProgramCounter(i) for i in range(players)]
        self.memmory = [Instruction() for j in range(memmorySize)]
        self.size = memmorySize
    def load(self, position, code):
        codeLength = len(code)
        self.memmory = self.memmory[0:position] + code + self.memmory[(position + codeLength):]
    def tick(self): #will return true if only one player remains
        self.setROM()
        nextInstruction = self.memmory[self.playerCounters[self.currentPlayer].currentPointer()]
        if(self.execute(nextInstruction)):
            #TODO: feed out that a player has lost even if the game is not over (relevant for more than two players)
            self.playerCounters.pop(self.currentPlayer)
            remain = len(self.playerCounters)
            if(remain == 1):
                return True
            self.currentPlayer %= remain
        else:
            self.currentPlayer = (self.currentPlayer + 1)%len(self.playerCounters)
        return False
        
    def execute(self, instruction):   #will return true if the player has lost his last thread
        #TODO: execute instructions. Should edit self.memmory and call advancePointer and/or advanceThread if relevant
        if(instruction.name == "nop"): #do nothing. Duh
            self.playerCounters[self.currentPlayer].advanceBoth(self.size)
            return False
        elif(instruction.name == "move"): # move
            a = self.getInstruction(instruction.values[0])
            b = self.getLocation(instruction.values[1])
            if(b == -1): #invalid destination, kills thread
                return self.playerCounters[self.currentPlayer].killCurrentPointer()
            else:
                self.memmory[b] = a
                self.playerCounters[self.currentPlayer].advanceBoth(self.size)
        return False
    def getInstruction(self, valueTuple): #returns the instruction in the relevent location (or makes the pseudo data for literals)
        if(valueTuple[1] == ""):
            return Instruction("data", [valueTuple])
        elif(valueTuple[1] == "@"):
            return self.memmory[valueTuple[0]]
        elif(valueTuple[1] == "#"):
            return self.memmory[self.memmory[valueTuple[0]].values[0][0]]
        elif(valueTuple[1] == "$"):
            #TODO: stuff concerning read only stuff
            foo = 1
    def getLocation(self, valueTuple): #return -1 if not valid
        if(valueTuple[1] == ""):
            return -1
        elif(valueTuple[1] == "@"):
            return valueTuple[0]
        elif(valueTuple[1] == "#"):
            return self.memmory[valueTuple[0]].values[0][0]
        elif(valueTuple[1] == "$"):
            #TODO: stuff concerning read only stuff
            foo = 1
    def setROM(self):
        #TODO: set the read only memmory
        foo = 1    