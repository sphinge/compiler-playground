import sys
from Lexing.Lexer import Lexer
from Lexing.grammarHash import grammarHash
from Parsing.ParsingTable import ParsingTable
from Parsing.Parser import Parser
from SymboltableStack import SymboltableStack

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
        global C_BOILERPLATE
        # TODO: handle wrong inputs
        if len(sys.argv)>1:
            inputFilePath = sys.argv[1]
        else:
            inputFilePath="tests/ezC_sample.txt"
        
        if len(sys.argv)>2:
            outputFilePath = sys.argv[2]
        else:
            outputFilePath = f"{inputFilePath}.c"

        if len(sys.argv)>3:
            with open(sys.argv[3])as extra_file:
                string=extra_file.read()
                C_BOILERPLATE+=string

        lexer = Lexer(inputFilePath)
        lexer.generateTokens()
        print("\n\n LEXER OUTPUT: \n\n "+str(lexer.tokenList)+"\n\n")
        
        pTable = ParsingTable(grammarHash)
        pTable.constructParseTable()
        pTable.printTable()

        parser = Parser(lexer.tokenList, pTable)
        parser.parse()

        parse_tree = parser.getParseTree()
        program= parse_tree.execute_IRGeneration()
        with open(outputFilePath, "w") as output:
            output.write(C_BOILERPLATE.replace("$input$", program))
        parse_tree.print(DEBUG=True)


if __name__=="__main__":
    Compiler.main()
