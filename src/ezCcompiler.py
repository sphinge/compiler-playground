import sys

from Lexing.grammarHash import grammarHash
from Lexing.Lexer import Lexer
from Parsing.Parser import Parser
from Parsing.ParsingTable import ParsingTable
from Semantic.SDDFunctions import Label, reset_temp_count

# import re
# from Semantic.SDDFunctions import symbolTable
# from SymboltableStack import SymboltableStack

DEBUG = False
C_BOILERPLATE = """
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
    def run(input_content: str) -> str:
        global C_BOILERPLATE, DEBUG
        lexer = Lexer()
        lexer.generateTokens(input_content)
        if DEBUG:
            print("\n\n LEXER OUTPUT: \n\n " + str(lexer.tokenList) + "\n\n")

        pTable = ParsingTable(grammarHash)
        pTable.constructParseTable()
        if DEBUG:
            pTable.printSets()
            pTable.printTable()

        parser = Parser(lexer.tokenList, pTable)
        parser.parse()

        parse_tree = parser.getParseTree()
        program = parse_tree.execute_IRGeneration()

        programString = ""
        for line in program:
            if not line:
                continue
            line = line.strip()
            programString += line + " "
            if line.endswith(";") or line.endswith(":"):
                programString += "\n"

        if DEBUG:
            parse_tree.print(DEBUG)

        return C_BOILERPLATE.replace("$input$", programString)

    @staticmethod
    def run_deterministically(input_content: str) -> str:
        # TODO: Labels and Temp variables maintain state between separate compilations.
        #       This is a problem when running tests.
        #       We added state-resetting functions to run individual compilatons deterministically.
        Label.reset_number_of_labels()
        reset_temp_count()

        return Compiler.run(input_content)


if __name__ == "__main__":
    # TODO: handle wrong inputs
    if len(sys.argv) < 3:
        print("USAGE: python compiler.py Path/to/ezCscript.ezC Path/to/Coutput.c")
        sys.exit(1)
    inputFilePath = sys.argv[1]
    outputFilePath = sys.argv[2]
    input_content = open(inputFilePath, "r").read()
    output_content = Compiler.run(input_content)
    with open(outputFilePath, "w") as output:
        output.write(output_content)
