'''
Created on 7 Sep 2012

@author: Callum
'''


        
class PlayerProgramCounter:
    counters = [0]
    currentCounter = 0
    ID = -1
    def __init__(self, playerID):
        self.ID = playerID
    def currentPointer(self):
        return self.counters[self.currentCounter]
    def killCurrentPointer(self): # returns true if that was the last pointer
        self.counters.pop(self.currentCounter)
        remain = len(self.counters)
        if(remain > 0):
            self.currentCounter %=remain
            return False
        return True
    def jumpPointer(self, value):
        self.counters[self.currentCounter] = value
    def advancePointer(self, memmorySize):
        self.counters[self.currentCounter] = (self.counters[self.currentCounter] + 1)%memmorySize
    def advanceThread(self):
        self.currentCounter = (self.currentCounter+1)%len(self.counters)