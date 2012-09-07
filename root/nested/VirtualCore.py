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
    def __init__(self, memmorySize, players):
        self.playerCounters = [PlayerProgramCounter(i) for i in range(players)]
        self.memmory = [Instruction() for j in range(memmorySize)]
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
        #TODO: execute. Should edit self.memmory and call advancePointer and/or advanceThread if relevant
        return False
    def setROM(self):
        #TODO: set the read only memmory
        foo = 1    