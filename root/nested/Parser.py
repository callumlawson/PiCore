'''
Created on 7 Sep 2012
@author: Callum
'''
from Instruction import Instruction

#Will return false if there is an checkError in the users code - the program otherwise.

class Parser:
    
    instuctionArgNums = {'dat':1,'mov':2,'jmp':1,'jpi':3,'add':3,'sub':3,'mlt':3,'div':3,'bch':1,'nop':0, 'mod':3, 'nnd':3,'orr':3,'xor':3} #TODO
    
    def __init__(self,engine):  #Path of file to be parsed
        print "Parser Created" #TODO
        self.engine = engine
      
    def processInstruction(self, rawInstruction, lineNumber):
        token = rawInstruction.lower() #Put everything to lower case  
        if token == "data" or token == "dat": return "dat"
        elif token == "move" or token == "mov": return "mov"
        elif token == "jump" or token == "jmp": return "jmp"
        elif token == "jumpif" or token == "jpi": return "jpi"
        elif token == "subtract" or token == "sub": return "sub"
        elif token == "multiply" or token == "mlt": return "mlt"
        elif token == "divide" or token == "div": return "div"
        elif token == "branch" or token == "bch": return "bch"
        elif token == "noop" or token == "nop": return "nop"
        elif token == "mod" : return "mod"
        elif token == "nand" : return "nnd"
        elif token == "or" : return "or"
        elif token == "xor": return "xor"
        elif token == "add": return "add"
        else:
            self.errorMessages.append("Line: " + str(lineNumber+1) + " Not a recognised instruction: " + token)
            return False        
        
    def checkInstruction(self,instruction,args,lineNumber): #Check that the Instruction has right number of arguments/ is otherwise valid  #User should be given feedback
        if not self.instuctionArgNums[instruction] == len(args):
            self.errorMessages.append("Line: " + str(lineNumber+1) + " Instruction: " + instruction + " has wrong num of args")
            return False
        else: return True
                
        
    def processFile(self,path):
        program = []   
        labelDict = {}                                             #An empty list to hold the users program
        self.errorMessages = [] #Record of errors generated if any.
        
        def replaceLables(arg,currentlineNumber):
            if labelDict.has_key(arg):
                return (labelDict[arg] - currentlineNumber)
            else: return arg
        
        file = open(path,'r') 
        dictLineNumber = 0;
        #Build label dictionary
        for line in file:
            if ":" in line:
                labelDict[line.split(":")[0]] = dictLineNumber
            if not len((line.split("/") [0]).split()) == 0: # check the line has an instruction
                dictLineNumber+=1     
        #print "Dictionary: " + str(labelDict)
        
        lineNumber = 0;
        file = open(path,'r')     
        #Parse the lines
        for line in file:
            
            if ":" in line and "/" in line:
                splitLine = (line.split("/") [0]).split(":")
                tokens = splitLine[1].split()
                #print "line: " + str(lineNumber) + " has '/' ':'  " + str(tokens)  
            elif "/" in line:   
                tokens = (line.split("/") [0]).split()
                #print "line: " + str(lineNumber) + " has '/' " + str(tokens) 
            elif ":" in line:
                splitLine  = line.split(":")
                tokens = splitLine[1].split()
                #print "line: " + str(lineNumber) + " has ':'  " + str(tokens)  
            else:                                     
                tokens = line.split()    
                #print "line: " + str(lineNumber) + " has no spec chars " + str(tokens)  
                                                        
            if len(tokens) != 0:                                 #Do not continue to parse if the line is empty.
                instructionArguments = []
                                                   
                instruction = self.processInstruction(tokens[0],lineNumber) #The instruction is the first token changed to a lower case 3letter code.
                
                if not instruction == False:
                    arguments = tokens[1:]                           #The rest of the tokens are arguments
                                  
                    for argument in arguments:                       #for each argument of the instruction (1-3 currently)
                        if argument[0] == "@" or argument[0] == "#" or  argument[0] == "$":            
                            instructionArguments.append((argument[0],replaceLables(argument[1:],lineNumber)))
                        else: 
                            instructionArguments.append(("",replaceLables(argument[0:],lineNumber)))
                    if(self.checkInstruction(instruction, instructionArguments,lineNumber)):
                        program.append(Instruction(instruction,instructionArguments))
                
                lineNumber += 1
                 
        #print program
        #print labelDict
        
        for intr in program:
            print intr.toString()
        
        file.close()
        
        if self.errorMessages != []: #If there are errors record them and return false
            self.engine.errorMessages.append("Program name: " + (((path.split("\\").pop()).split("."))[0]))
            for message in self.errorMessages:
                self.engine.errorMessages.append(message)
            self.engine.errorMessages.append("Program will not run")
            return False
        else: return program
        

        
        
        