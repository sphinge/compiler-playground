from typing import Any

from Lexing.Lexer import Lexer, Token
from Lexing.TokenTypes import TokenType
from Parsing.ParsingTable import ParsingTable
from Parsing.Tree import Tree_Wrapper


class Parser:
    input: list[Token]
    table: ParsingTable
    stack: list[tuple[Any, Any]]
    tree: Tree_Wrapper

    def __init__(self, tokenList: list[Token], table: ParsingTable):
        self.input = tokenList
        self.ParsingTable = table
        self.stack = [("PROGRAM", 1)]
        self.tree = Tree_Wrapper()
        self.tree.addNode("PROGRAM")

    def getParseTree(self):
        return self.tree

    def parse(self):
        while self.input != []:
            self.parse_step()

        if self.stack == []:
            pass
            # print("DONE!")
            # print(self.stack)
            # self.tree.print()
        else:
            print(self.stack)
            print("Parsing Failed")

    def parse_step(self):
        lookahead = self.input[0]
        token = self.stack[0]

        if token[0] == "epsilon":
            self.stack.pop(0)
            return

        if type(token[0]) == TokenType and token[0] == lookahead[0]:
            self.stack.pop(0)
            self.input.pop(0)

            # If we have a literal value attached to the Token, append it to the respectiveNode
            if lookahead[1] is not None:
                Node = self.tree.find(token[1])
                Node.lexval = lookahead[1]

            # print("matched: ")
            # print(token)
            return

        elif type(token[0]) == TokenType:
            self.tree.print()
            raise Exception(f"EXPECTED: {token}, GOT:{lookahead}")

        production = self.ParsingTable.get_table_entry(token[0], lookahead[0])
        if self.stack[0][0] == "ELEVEL5X":
            pass
        if production == []:
            self.tree.print()
            raise Exception(f"EXPECTED: {token}, GOT:{lookahead}")

        self.stack.pop(0)
        stack_acc = []

        for i in production:
            if not type(i) == TokenType:
                id = self.tree.addNode(i, token[1])
                stack_acc.append((i, id))
            else:
                id = self.tree.addNode(TokenType.token_type_to_string(i), token[1])
                stack_acc.append((i, id))

        self.tree.add_SDD_function_handles(token, production)
        self.stack = stack_acc + self.stack


if __name__ == "__main__":
    from Lexing.grammarHash import grammarHash

    file_content = open("ezctest.txt", "r").read()

    lexer = Lexer()
    lexer.generateTokens(file_content)

    parseTable = ParsingTable(grammarHash)
    parseTable.constructParseTable()
    parseTable.printTable()
    p = Parser(lexer.tokenList, parseTable)
    p.parse()
