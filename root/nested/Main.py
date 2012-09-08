'''
Created on 7 Sep 2012

@author: Callum
'''

import Parser

if __name__ == '__main__':
    
    #Test Parser
    parser = Parser.Parser()
    for instruction in  parser.processFile("demoCode.txt"):
        print instruction.printInstruction()
        
    pass