'''
Created on 7 Sep 2012

@author: Callum
'''
class Instruction:
    
    def __init__(self, instructionName = "nop", instructionArguments = [("", 0)], creator = -1):
        self.name = instructionName
        self.arguments = instructionArguments
        self.lastMod = creator
    def printInstruction(self):
        return self.name + " " + " ".join(map(str, self.arguments))
