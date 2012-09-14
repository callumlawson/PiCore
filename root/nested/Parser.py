'''
Created on 7 Sep 2012

@author: Callum
'''
from Instruction import Instruction

class Parser:
    
    instuctionArgumentNumbers = {'dat':1,'mov':2,'jmp':1,'jpi':3,'add':3,'sub':3,'mlt':3,'div':3,'bch':1,'nop':0} #TODO
    
    def __init__(self):  #Path of file to be parsed
        print "Parser Created" #TODO

    def processInstruction(self, rawInstruction):
        token = rawInstruction.lower() #Put everything to lower case  
        if token == "data" or token == "dat": return "dat"
        elif token == "move" or token == "mov": return "mov"
        elif token == "jump" or token == "jmp": return "jmp"
        elif token == "jumpif" or token == "jpi": return "jpi"
        elif token == "add": return "add"
        elif token == "subtract" or token == "sub": return "sub"
        elif token == "multiply" or token == "mlt": return "mlt"
        elif token == "divide" or token == "div": return "div"
        elif token == "branch" or token == "bch": return "bch"
        elif token == "noop" or token == "nop": return "nop"
        else: self.error("Non recognised instuction: " + token)
        
    def checkInstruction(self,Instruction): #Check that the Instruction has right number of arguments/ is otherwise valid
        pass #TODO                       #User should be given feedback

    def error(self, message):
        print message
        pass #TODO
        
    def processFile(self,path):
    
        file = open(path,'r') 
        program = []                                                 #An empty list to hold the users program
        
        for line in file:
            
            if "/" in line:   
                tokens = (line.split("/") [0]).split()
            else:   
                #print line.split()                                  
                tokens = line.split()    
                                                        
            if len(tokens) != 0:                                 #Do not continue to parse if the line is empty.
                instructionArguments = []
                                                   
                instruction = self.processInstruction(tokens[0]) #The instruction is the first token changed to a lower case 3letter code.
                    #TODO abort if not recognised... do in error?
                arguments = tokens[1:]                           #The rest of the tokens are arguments
                              
                for argument in arguments:                       #for each argument of the instruction (1-3 currently)
                    if argument[0] == "@" or argument[0] == "#" or  argument[0] == "$":             
                        instructionArguments.append((argument[0],argument[1:]))
                    else: 
                        instructionArguments.append(("",argument[0:]))
                    
                program.append(Instruction(instruction,instructionArguments))
                    
        file.close()
        return program
        


        
        
        