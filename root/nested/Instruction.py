'''
Created on 7 Sep 2012

@author: Callum
'''
class Instruction:
    
    #(Modifier, Value) e.g [("@",5),("#",1)]
    
    def __init__(self, instructionName = "nop", instructionArguments = [("", 0)], creator = -1):
        self.name = instructionName
        self.arguments = instructionArguments
        self.lastMod = creator
    def toString(self):
        return self.name + " " + " ".join(map(str, self.arguments))
    def clone(self):
        newArgs = []
        for oldArg in self.arguments:
            newArgs.append((oldArg[0],oldArg[1]))
        return Instruction(self.name,newArgs,self.lastMod)
