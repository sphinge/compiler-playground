from lexer import Lexer
from symboltableStack import SymboltableStack
from Parser.ParsingTable import ParsingTable
from Parser.grammarHash import grammarHash
from MyParser import MyParser
import sys
class Compiler:
    @staticmethod
    def main():
        # TODO: handle wrong inputs
        if len(sys.argv)>1:
            ezcFilePath = sys.argv[1]
        else:
            ezcFilePath="src/ezctest.txt"
        lexer = Lexer(ezcFilePath)
        lexer.generateTokens()
        print(lexer.tokenList)
        
        pTable=ParsingTable(grammarHash)
        pTable.constructParseTable()
        pTable.printTable()
        print(pTable.parseTable["PROGRAM"])
        parser= MyParser(lexer.tokenList, pTable)
        parser.parse()



if __name__=="__main__":
    Compiler.main()
