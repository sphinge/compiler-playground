from Lexing.Lexer import Lexer
from Lexing.TokenTypes import TokenType


def test_lexer():
    test_code = """;
2;
"asdffa"
32345.123
(){};
var i <=23;
var j =(i +1) * 2; // alksdjhfkj<<<=>//()
"""
    lexer = Lexer()
    lexer.generateTokens(test_code)
    tokens = lexer.tokenList
    assert tokens == [
        (TokenType.SEMICOLON, None),
        (TokenType.INT, 2),
        (TokenType.SEMICOLON, None),
        (TokenType.STRING, "asdffa"),
        (TokenType.FLOAT, 32345.123),
        (TokenType.LEFT_PAREN, None),
        (TokenType.RIGHT_PAREN, None),
        (TokenType.LEFT_BRACE, None),
        (TokenType.RIGHT_BRACE, None),
        (TokenType.SEMICOLON, None),
        (TokenType.VAR, None),
        (TokenType.IDENTIFIER, "i"),
        (TokenType.LESS_EQUAL, None),
        (TokenType.INT, 23),
        (TokenType.SEMICOLON, None),
        (TokenType.VAR, None),
        (TokenType.IDENTIFIER, "j"),
        (TokenType.EQUAL, None),
        (TokenType.LEFT_PAREN, None),
        (TokenType.IDENTIFIER, "i"),
        (TokenType.PLUS, None),
        (TokenType.INT, 1),
        (TokenType.RIGHT_PAREN, None),
        (TokenType.STAR, None),
        (TokenType.INT, 2),
        (TokenType.SEMICOLON, None),
        (TokenType.EOF, None),
    ]
