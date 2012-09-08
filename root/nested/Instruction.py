'''
Created on 7 Sep 2012

@author: Callum
'''
class Instruction:
    
    name = "nop"
    arguments = [("", 0)]   #(Modifier, Value) e.g [("@",5),("#",1)]
    
    def __init__(self, instructionName = "nop", instructionArguments = [("", 0)]):
        self.name = instructionName
        self.arguments = instructionArguments
        
    def printInstruction(self):
        return self.name + " " + " ".join(map(str, self.arguments))