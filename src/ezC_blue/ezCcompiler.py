import sys
import re
#print(sys.path[0])
from Lexing.Lexer import Lexer
from Lexing.grammarHash import grammarHash
from Parsing.ParsingTable import ParsingTable
from Parsing.Parser import Parser
from SymboltableStack import SymboltableStack
from Semantic.SDDFunctions import symbolTable

DEBUG=False
DEBUG2= True
C_BOILERPLATE="""
#ifndef CUSTOM_STDIO_H
#define CUSTOM_STDIO_H

#include <stdio.h>
#include <string.h>
#include <stdbool.h>

$import$

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
        inputFilePath="input.ezC"
        outputFilePath = "out.c"
        #print(sys.argv)
        if len(sys.argv) >1:
            c_import_file_name=f'#include "{sys.argv[1]}"'
        else:
            c_import_file_name = ""
        #print(c_import_file_name)
                    
        if c_import_file_name != "":
            with open(sys.argv[1], "r")as extra_file:
                string=extra_file.read()
                #print(string)
                Compiler.put_functions_into_SymbolTable(string)

        C_BOILERPLATE=C_BOILERPLATE.replace("$import$", c_import_file_name)
        

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
        with open(outputFilePath, "w") as output:
            output.write(C_BOILERPLATE.replace("$input$", program))
        
        print(C_BOILERPLATE)
        if DEBUG:            
            parse_tree.print(DEBUG)

    @staticmethod
    def put_functions_into_SymbolTable(file:str):
        pattern = r"\$ezC:.+?\-\>.+?\$"

        entries=[]
        matches = re.findall(pattern, file)
        for match in matches:
            match=match.replace("$ezC:","")
            match=match.replace("$","")
            if DEBUG:
                print(match)
            entry= match.split("->")
            symbolTable.addSymbolToCurrentContext(entry[0], None, entry[1])
        if DEBUG:
            symbolTable.print()

if __name__=="__main__":
    Compiler.main()
