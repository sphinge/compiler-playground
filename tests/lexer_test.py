from lexer import Lexer
from TokenTypes import TokenType


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
    lexer.run(test_code)
    tokens = lexer.tokenList
    assert tokens == [
        [TokenType.SEMICOLON.name, None],
        [TokenType.NUMBER.name, 2.0],
        [TokenType.SEMICOLON.name, None],
        [TokenType.STRING.name, "asdffa"],
        [TokenType.NUMBER.name, 32345.123],
        [TokenType.LEFT_PAREN.name, None],
        [TokenType.RIGHT_PAREN.name, None],
        [TokenType.LEFT_BRACE.name, None],
        [TokenType.RIGHT_BRACE.name, None],
        [TokenType.SEMICOLON.name, None],
        [TokenType.VAR.name, None],
        [TokenType.IDENTIFIER.name, "i"],
        [TokenType.LESS_EQUAL.name, None],
        [TokenType.NUMBER.name, 23.0],
        [TokenType.SEMICOLON.name, None],
        [TokenType.VAR.name, None],
        [TokenType.IDENTIFIER.name, "j"],
        [TokenType.EQUAL.name, None],
        [TokenType.LEFT_PAREN.name, None],
        [TokenType.IDENTIFIER.name, "i"],
        [TokenType.PLUS.name, None],
        [TokenType.NUMBER.name, 1.0],
        [TokenType.RIGHT_PAREN.name, None],
        [TokenType.STAR.name, None],
        [TokenType.NUMBER.name, 2.0],
        [TokenType.SEMICOLON.name, None],
        [TokenType.EOF.name, None],
    ]
