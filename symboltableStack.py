class Symboltable:
    def __init__(self, parent):
        self.table = {}
        self.parent = parent # Symbol table of outer scope

    def add(self, symbol, value):
        self.table[symbol] = value

class SymboltableStack:
    def __init__(self):
        self.globalTable = Symboltable(None)
        self.head = self.globalTable
        self.prev = None # previous stack element, NOT necessarily parent of symbol table

    def pushNewTableOnCurrentContext(self):
        newSymbolTable = Symboltable(parent= self.head)
        self.prev = self.head   
        self.head = newSymbolTable

    def pushNewTableOnGolbalContext(self):
        newSymbolTable = Symboltable(parent= self.globalTable)
        self.prev = self.head
        self.head = newSymbolTable

    def addSymbolToCurrentContext(self, symbol, value):
        self.head.add(symbol, value)

    def popHead(self):
        self.head = self.prev
        #old 'self.head' is garbage-collected

    def get(self, key):
        chainElement = self.head

        while key not in chainElement.table:
            if chainElement.parent == None:
                return None
            else:
                chainElement = chainElement.parent

        return chainElement.table[key] # None if id not contained in any symbol table
    