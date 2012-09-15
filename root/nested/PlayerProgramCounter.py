'''
Created on 7 Sep 2012

@author: Callum
'''


        
class PlayerProgramCounter:
    
    
    def __init__(self,owner, playerID, startPointer = 0):
        self.ID = playerID
        self.counters = [startPointer]
        self.currentCounter = 0
        self.core = owner
        self.core.ROM[1] +=1
        self.core.ROM[2] +=1
    def currentPointer(self):
        return self.counters[self.currentCounter]
    
    def killCurrentPointer(self): # returns true if that was the last pointer
        self.core.ROM[2] -=1
        self.counters.pop(self.currentCounter)
        remain = len(self.counters)
        if(remain > 0):
            self.currentCounter %=remain
            return False
        self.core.ROM[1] -=1
        return True
    
    def jumpPointer(self, value):
        self.counters[self.currentCounter] = value
        self.core.changesList.append(value)
    def advancePointer(self):
        self.counters[self.currentCounter] = (self.counters[self.currentCounter] + 1)%self.core.size
        self.core.changesList.append(self.counters[self.currentCounter])
    def advanceThread(self):
        self.currentCounter = (self.currentCounter+1)%len(self.counters)
        
    def advanceBoth(self):
        self.advancePointer()
        self.advanceThread()
        
    def spawnThread(self, at):
        self.core.ROM[2] +=1
        self.core.changesList.append(at)
        self.counters.insert(self.currentCounter+1, at)