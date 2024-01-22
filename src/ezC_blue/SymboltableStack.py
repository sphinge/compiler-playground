class SymboltableStackItem:
    def __init__(self, parent, previous):
        self.table = {}
        self.parent = parent # Symbol table of outer scope
        self.previous = previous

    def add(self, symbol, value, type):
        self.table[symbol] = {"value":value, "type":type}

class SymboltableStack:
    def __init__(self):
        self.globalTable = SymboltableStackItem(None, None)
        self.head = self.globalTable

    def pushNewTableOnCurrentContext(self):
        newSymbolTable = SymboltableStackItem(parent= self.head, previous= self.head)
        self.head = newSymbolTable

    def pushNewTableOnGlobalContext(self):
        newSymbolTable = SymboltableStackItem(parent= self.globalTable, previous= self.head)
        self.head = newSymbolTable

    def addSymbolToCurrentContext(self, symbol, value, type):
        self.head.add(symbol, value, type)

    def popHead(self):
        self.head = self.head.previous
        #old 'self.head' is garbage-collected

    def get(self, key):
        chainElement = self.head

        while key not in chainElement.table:
            if chainElement.parent == None:
                return None
            else:
                chainElement = chainElement.parent

        return chainElement.table[key] # None if id not contained in any symbol table
