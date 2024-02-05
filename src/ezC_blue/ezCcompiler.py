import sys
import re
#print(sys.path[0])
from Lexing.Lexer import Lexer
from Lexing.grammarHash import grammarHash
from Parsing.ParsingTable import ParsingTable
from Parsing.Parser import Parser
from SymboltableStack import SymboltableStack
from Semantic.SDDFunctions import symbolTable

DEBUG=True
C_BOILERPLATE="""
#ifndef CUSTOM_STDIO_H
#define CUSTOM_STDIO_H

#include <stdio.h>
#include <string.h>
#include <stdbool.h>

int main() {
$input$
}
#endif // CUSTOM_STDIO_H
"""

class Compiler:

    @staticmethod
    def main():
        global C_BOILERPLATE, DEBUG
        # TODO: handle wrong inputs
        if len(sys.argv) < 3:
            print("USAGE: python compiler.py Path/to/ezCscript.ezC Path/to/Coutput.c")
            return 1
        inputFilePath = sys.argv[1]
        outputFilePath= sys.argv[2]
        lexer = Lexer(inputFilePath)
        lexer.generateTokens()
        if DEBUG:
            print("\n\n LEXER OUTPUT: \n\n "+str(lexer.tokenList)+"\n\n")
        
        pTable = ParsingTable(grammarHash)
        pTable.constructParseTable()
        if DEBUG:
            pTable.printSets()
            pTable.printTable()

        parser = Parser(lexer.tokenList, pTable)
        parser.parse()

        parse_tree = parser.getParseTree()
        program= parse_tree.execute_IRGeneration()
        
        programString = ""
        for line in program:
            if line ==[]:
                continue
            line = line.strip()
            programString+=  line+" "
            if line.endswith(";") or line.endswith(":"):        
                programString+="\n"                
        
        with open(outputFilePath, "w") as output:
            output.write(C_BOILERPLATE.replace("$input$",programString))
        
        if DEBUG:            
            parse_tree.print(DEBUG)



if __name__=="__main__":
    Compiler.main()
