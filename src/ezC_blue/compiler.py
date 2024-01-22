import sys
from Lexing.Lexer import Lexer
from Lexing.grammarHash import grammarHash
from Parsing.ParsingTable import ParsingTable
from Parsing.Parser import Parser
from SymboltableStack import SymboltableStack

class Compiler:

    @staticmethod
    def main():
        # TODO: handle wrong inputs
        if len(sys.argv)>1:
            ezcFilePath = sys.argv[1]
        else:
            ezcFilePath="tests/ezC_sample.txt"
            
        lexer = Lexer(ezcFilePath)
        lexer.generateTokens()
        print("\n\n LEXER OUTPUT: \n\n "+str(lexer.tokenList)+"\n\n")
        
        pTable = ParsingTable(grammarHash)
        pTable.constructParseTable()
        pTable.printTable()

        parser = Parser(lexer.tokenList, pTable)
        parser.parse()

        parse_tree = parser.getParseTree()

        print(parse_tree.execute_IRGeneration())



if __name__=="__main__":
    Compiler.main()
