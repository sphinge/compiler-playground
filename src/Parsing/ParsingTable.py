from src.Lexing.grammarHash import grammarHash
from src.Lexing.TokenTypes import TokenType

class ParsingTable:
    def __init__(self, grammarHashTable, separatorSymbol = '|', endSymbol = 'eof', startSymbol = None, epsilon = 'epsilon'):
        self.parseTable      = {}
        self.FIRST           = {}
        self.FOLLOW          = {}
        self.grammar         = grammarHashTable
        self.nonTerminals    = list(self.grammar.keys())
        self.separatorSymbol = separatorSymbol
        self.endSymbol       = endSymbol
        self.startSymbol     = startSymbol if startSymbol != None else self.nonTerminals[0]
        self.epsilon         = epsilon

        self.initParseTable()
        self.initSets()
        self.generateSets()
        self.printSets()

    def get_table_entry(self, NonTerminal:str, token:TokenType):
        production=[]
        token_string=TokenType.token_type_to_string(token)
        try:
            entry= self.parseTable[NonTerminal][token_string.lower()]
        except: 
            return []
        for word in entry.split(" "):
            token= TokenType.string_to_token_type(word.upper())
            if not token:  
                # Couldnt match token type, therefore its a NonTerminal
                production.append(word)
            else:
                # Could match tokentype, therefore its a terminal
                production.append(token)
        return production            # Could match tokentype, therefore its a terminal

    def initParseTable(self):
        for nonTerminal in self.nonTerminals:
            self.parseTable[nonTerminal] = {}
    
    def initSets(self):
        for nonTerminal in self.nonTerminals:
            self.FIRST[nonTerminal] = set()
            self.FOLLOW[nonTerminal] = set()
            self.FOLLOW[self.startSymbol] = self.FOLLOW[self.startSymbol].union({self.endSymbol})

    def constructParseTable(self):
        for nonTerminal in self.nonTerminals:
            productions = self.grammar[nonTerminal].split(self.separatorSymbol)


            #for each production A->alpha of the grammar, do the following... (according to lecture book)
            for production in productions:
                symbols = production.split(' ')
                productionFirstSet = self.FIRST[symbols[0]] if self.isNonTerminalSymbol(symbols[0]) else [symbols[0]]

                #2. If epsilon is in FIRST(alpha), then for each terminal b in FOLLOW(A), add A->alpha to M[A,b]. If alpha is in
                #FIRST(alpha) and $ is in FOLLOW(A), add A->alpha to M[A,$] as well.
                if not self.epsilon in productionFirstSet:
                    for terminal in productionFirstSet:
                        if terminal == self.epsilon:
                            continue
                        self.parseTable[nonTerminal][terminal] = production
                else:
                    if self.endSymbol in self.FOLLOW[nonTerminal]:
                            self.parseTable[nonTerminal][self.endSymbol] = production
                    for terminal in self.FOLLOW[nonTerminal]:
                        try:
                            self.parseTable[nonTerminal][terminal] 
                        except:
                            self.parseTable[nonTerminal][terminal] = production
                

    def generateSets(self):
        for nonTerminal in self.nonTerminals:
            self.constructFirstSet(nonTerminal)

        old_follow = None
        while self.followHasChanged(old_follow):
            old_follow = self.copyFollow(self.FOLLOW)
            for nonTerminal in self.nonTerminals:
                self.constructFollowSet(nonTerminal)

    def constructFirstSet(self, nonTerminal):
        productions = self.grammar[nonTerminal].split(self.separatorSymbol) #e.g.  * F T´ | €  will be converted to [[* F T´], [€]]

        for production in productions:
            symbols = production.split(' ')
            for symbol in symbols:
                if self.isNonTerminalSymbol(symbol):
                    self.constructFirstSet(symbol)
                    self.FIRST[nonTerminal] = self.FIRST[nonTerminal].union(self.FIRST[symbol])
                    if self.epsilon not in self.FIRST[symbol]:
                        break
                else:
                    if symbol not in self.FIRST[nonTerminal]:
                        self.FIRST[nonTerminal] = self.FIRST[nonTerminal].union({symbol})
                    break
        

    def constructFollowSet(self, nonTerminal):
        for nonTerminalToCheck in self.nonTerminals:
            if nonTerminalToCheck == nonTerminal: 
                continue

            productions = self.grammar[nonTerminalToCheck].split(self.separatorSymbol)

            for production in productions:
                symbols = production.split(" ")
                followSetCandidate = False # might the current symbol be used to change the follow-set of our NT

                checkNextNonTerminal = True

                for symbol in symbols:
                    if symbol == nonTerminal:
                        followSetCandidate = True
                        continue

                    if not followSetCandidate:
                        continue
                    
                    if checkNextNonTerminal == False:
                        continue
                    else:
                        checkNextNonTerminal = False

                    if self.isNonTerminalSymbol(symbol):
                        self.FOLLOW[nonTerminal] = self.FOLLOW[nonTerminal].union(self.FIRST[symbol].difference({self.epsilon}))
                        if self.epsilon in self.FIRST[symbol]:
                            self.FOLLOW[nonTerminal] = self.FOLLOW[nonTerminal].union(self.FOLLOW[nonTerminalToCheck])
                        else: # symbol cannot produce epsilon
                            followSetCandidate = False
                    else: # symbol is terminal symbol
                        if symbol != self.epsilon:
                            self.FOLLOW[nonTerminal] = self.FOLLOW[nonTerminal].union({symbol}.difference({self.epsilon}))
                            followSetCandidate = False

                # end for symbols
                if followSetCandidate:
                    self.FOLLOW[nonTerminal] = self.FOLLOW[nonTerminal].union(self.FOLLOW[nonTerminalToCheck])

    def isNonTerminalSymbol(self, symbol):
        return symbol in self.nonTerminals

    def followHasChanged(self, comp):
        if comp == None:
            return True
        for key, val in comp.items():
            if (self.FOLLOW[key] != val):
                return True
        return False

    def copyFollow(self, follow):
        result = {}
        for key, val in follow.items():
            result[key] = val.copy()
        return result

    def printSets(self):
        print("\n///////////FIRST-SETS///////////")
        for key in self.nonTerminals:
            print(key + ": " + str(self.FIRST[key]))

        print("\n///////////FOLLOW-SETS///////////")
        for key in self.nonTerminals:
            print(key + ": " + str(self.FOLLOW[key]))

    def printTable(self):
        print("\n///////////PARSE-TABLE///////////")
        for nonTerminal in self.nonTerminals:
            print(nonTerminal + ":")
            for key in self.parseTable[nonTerminal].keys():
                print("    " + key + ": " + self.parseTable[nonTerminal][key])


#----TEST----#
    
if __name__ == "__main__":
    parseTable = ParsingTable(grammarHash)
    parseTable.constructParseTable()
    parseTable.printTable()
    
    print(parseTable.get_table_entry("E_LEVEL3", TokenType.EOF))

    print(parseTable.get_table_entry("DECLARATION", TokenType.IF))