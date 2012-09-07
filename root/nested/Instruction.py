'''
Created on 7 Sep 2012

@author: Callum
'''
class Instruction:
    name = ""
    values = []
    valueMods = []
    def __init__(self, instructionName = "nop", instructionValues = [0], instructionMods = [""]):
        self.name = instructionName
        self.values = instructionValues
        self.valueMods = instructionMods