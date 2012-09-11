'''
Created on 7 Sep 2012

@author: Callum
'''
class Instruction:
    
    name = "nop"
    arguments = [("", 0)]   #(Modifier, Value) e.g [("@",5),("#",1)]
    lastMod = -1
    def __init__(self, instructionName = "nop", instructionArguments = [("", 0)], creator = -1):
        self.name = instructionName
        self.arguments = instructionArguments
        self.lastMod = creator
    def printInstruction(self):
        return self.name + " " + " ".join(map(str, self.arguments))