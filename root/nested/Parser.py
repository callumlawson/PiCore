'''
Created on 7 Sep 2012

@author: Callum
'''

class Parser:
    
    def __init__(self, Path):  #Path of file to be parsed
        file = open(Path,'r')
        for line in file:
            print line
            
        file.close()