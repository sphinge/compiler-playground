from lexer import Lexer
from symboltableStack import SymboltableStack

class Compiler:
    def __init__(self, filePath):

        self.symboltableStack = SymboltableStack()
        self.lexer = Lexer(filePath)
        #self.parser = Parser()
