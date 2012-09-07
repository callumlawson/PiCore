'''
Created on 7 Sep 2012

@author: Callum
'''
class Instruction:
    
    name = "nop"
    values = [("", 0)]   #(Modifier, Value) e.g [("@",5),("#",1)]
    
    def __init__(self, instructionName = "nop", instructionValues = [("", 0)]):
        self.name = instructionName
        self.values = instructionValues