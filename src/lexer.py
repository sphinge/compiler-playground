from TokenTypes import TokenType

keywords = {
    "and": TokenType.AND,
    "class": TokenType.CLASS,
    "else": TokenType.ELSE,
    "false": TokenType.FALSE,
    "for": TokenType.FOR,
    "func": TokenType.FUNC,
    "if": TokenType.IF,
    "nil": TokenType.NIL,
    "or": TokenType.OR,
    "print": TokenType.PRINT,
    "return": TokenType.RETURN,
    "super": TokenType.SUPER,
    "this": TokenType.THIS,
    "true": TokenType.TRUE,
    "var": TokenType.VAR,
    "while": TokenType.WHILE,
}


class Lexer:
    def __init__(self):
        self.tokenList = []
        self.lexemeBegin = 0
        self.forward = 0
        self.currentLine = ""

    def run(self, input_string: str):
        self.tokenList = []  # Reset the token list for new input
        for self.currentLine in input_string.splitlines(keepends=True):
            self.scanTokens()
            self.reset()
        self.tokenList.append([TokenType.EOF.name, None])

    def reachedEnd(self):
        return self.forward == len(self.currentLine) - 1

    def advance(self):
        if not self.reachedEnd():
            self.forward = self.forward + 1

    def reset(self):
        self.lexemeBegin = 0
        self.forward = 0

    def moveToNextLexeme(self):
        self.advance()
        self.lexemeBegin = self.forward

    def peek(self):
        return self.currentLine[self.forward]

    def lookahead(self):
        if not self.reachedEnd():
            return self.currentLine[self.forward + 1]
        else:
            return ""  # no lookahead possible if forward reached last character of currentLine

    def consumeToken(self, type, literal=None):
        self.tokenList.append([type.name, literal])
        self.moveToNextLexeme()

    def isDigit(self, char):
        cond1 = char >= "0"
        cond2 = char <= "9"
        return cond1 and cond2

    def isAlpha(self, char):
        cond1 = char >= "a" and char <= "z"
        cond2 = char >= "A" and char <= "Z"
        cond3 = char == "_"
        return cond1 or cond2 or cond3

    def isAlphaNumeric(self, char):
        cond1 = self.isAlpha(char)
        cond2 = self.isDigit(char)
        return cond1 or cond2

    def isMultiOperator(self):
        if self.lookahead() == "=":
            self.advance()
            return True
        else:
            return False

    def skipComment(self):
        while self.peek() != "\n" and not self.reachedEnd():
            self.advance()

    def handleString(self):
        while self.lookahead() != '"' and not self.reachedEnd():
            if self.lookahead() == "\n":
                print("missing closing asterix")
                return
            else:
                self.advance()

        if self.reachedEnd():
            print("missing closing asterix")
            return

        self.advance()
        stringValue = self.currentLine[self.lexemeBegin + 1 : self.forward]
        self.consumeToken(TokenType.STRING, stringValue)

    def handleNumber(self):
        while self.isDigit(self.lookahead()):
            self.advance()

        if self.lookahead() == ".":
            self.advance()
            if self.isDigit(self.lookahead()):
                while self.isDigit(self.lookahead()):
                    self.advance()
            else:
                print("decimalpoint must be followed by digit")
                return
        self.consumeToken(
            TokenType.NUMBER,
            float(self.currentLine[self.lexemeBegin : self.forward + 1]),
        )

    def handleIdentifier(self):
        while self.isAlphaNumeric(self.peek()):
            self.advance()

        identifier = self.currentLine[self.lexemeBegin : self.forward]

        keyword = keywords.get(identifier)  # test if identifier matches any keyword
        if keyword:
            self.consumeToken(keyword)
        else:
            self.consumeToken(TokenType.IDENTIFIER, identifier)

    def scanTokens(self):
        self.reset()
        while not self.reachedEnd():
            match self.peek():
                case "(":
                    self.consumeToken(TokenType.LEFT_PAREN)
                case ")":
                    self.consumeToken(TokenType.RIGHT_PAREN)
                case "{":
                    self.consumeToken(TokenType.LEFT_BRACE)
                case "}":
                    self.consumeToken(TokenType.RIGHT_BRACE)
                case ",":
                    self.consumeToken(TokenType.COMMA)
                case ".":
                    self.consumeToken(TokenType.DOT)
                case "-":
                    self.consumeToken(TokenType.MINUS)
                case "+":
                    self.consumeToken(TokenType.PLUS)
                case ";":
                    self.consumeToken(TokenType.SEMICOLON)
                case "*":
                    self.consumeToken(TokenType.STAR)
                case "!":
                    self.consumeToken(
                        TokenType.BANG_EQUAL
                    ) if self.isMultiOperator() else self.consumeToken(TokenType.BANG)
                case "=":
                    self.consumeToken(
                        TokenType.EQUAL_EQUAL
                    ) if self.isMultiOperator() else self.consumeToken(TokenType.EQUAL)
                case "<":
                    self.consumeToken(
                        TokenType.LESS_EQUAL
                    ) if self.isMultiOperator() else self.consumeToken(TokenType.LESS)
                case ">":
                    self.consumeToken(
                        TokenType.GREATER_EQUAL
                    ) if self.isMultiOperator() else self.consumeToken(
                        TokenType.GREATER
                    )
                case "/":
                    self.consumeToken(
                        TokenType.SLASH
                    ) if self.lookahead() != "/" else self.skipComment()
                case " ":
                    self.moveToNextLexeme()
                case "\r":
                    self.moveToNextLexeme()
                case "\t":
                    self.moveToNextLexeme()
                case "\n":
                    self.moveToNextLexeme()
                case '"':
                    self.handleString()
                case __:
                    if self.isDigit(self.peek()):
                        self.handleNumber()
                    elif self.isAlpha(self.peek()):
                        self.handleIdentifier()
                    else:
                        print(self.currentLine, "unexpected character.")
                        self.moveToNextLexeme()
