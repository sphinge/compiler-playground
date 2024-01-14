from Tree import Tree_Wrapper
from TokenTypes import TokenType

from Parser.stringMatcher import Matcher

class MyParser:
    def __init__(self, tokenstrem, table):
        self.input=tokenstrem
        self.ParsingTable=table
        self.stack= [("PROGRAM", 1)]
        self.tree=Tree_Wrapper()
        self.tree.addNode("PROGRAM")

    def parse_step(self):
        lookahead=self.input[0]
        token=self.stack[0]
        if token[0] == "epsilon":
            self.stack.pop(0)
            return
        if type(token[0])==TokenType and token[0]==lookahead[0]:
            self.stack.pop(0)
            self.input.pop(0)
            print("matched: ")
            print(token)
            return
        elif type(token[0])==TokenType:
            self.tree.print()
            raise Exception(f"EXPECTED: {token}, GOT:{lookahead}")
        production=self.ParsingTable.get_table_entry(token[0], lookahead[0])
        if production == []:
            self.tree.print()
            raise Exception(f"EXPECTED: {token}, GOT:{lookahead}")
        self.stack.pop(0)
        stack_acc=[]
        for i in (production):
            if not type(i)==TokenType:
                id=self.tree.addNode(i, token[1])
                stack_acc.append((i, id))

            else:
                id= self.tree.addNode(Matcher.token_type_to_string(i), token[1])
                stack_acc.append((i, id))
        self.tree.add_SDD_handler(token, production)
        self.stack= stack_acc+self.stack
        

    def parse(self):
        while self.input[0][0]!=TokenType.EOF or self.stack[0][0]!="PROGRAMX":
            self.parse_step()
        if self.stack[0][0]=="PROGRAMX" and len(self.stack)==1:
            print("DONE!")
            print(self.stack)
            self.tree.addNode("epsilon", self.stack[0][1])
            self.tree.print()
            self.tree.generate_AST()
        else: 
            print(self.stack)
            print("Parsing Failed")


if __name__=="__main__":
    from Parser.ParsingTable import ParsingTable
    from Parser.grammarHash import grammarHash
    from lexer import Lexer
    l= Lexer("ezctest.txt")
    l.generateTokens()

    parseTable = ParsingTable(grammarHash)
    parseTable.constructParseTable()
    parseTable.printTable()
    p= MyParser(l.tokenList, parseTable)
    p.parse()