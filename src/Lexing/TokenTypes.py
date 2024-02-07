from enum import Enum
from typing import Optional


class TokenType(Enum):
    EOF = (0,)

    LEFT_PAREN = (1,)
    RIGHT_PAREN = (2,)
    LEFT_BRACE = (3,)
    RIGHT_BRACE = (4,)
    COMMA = (5,)
    DOT = (6,)
    MINUS = (7,)
    PLUS = (8,)
    SEMICOLON = (9,)
    SLASH = (10,)
    STAR = (11,)
    VERTICAL_BAR = (12,)

    BANG = (13,)
    BANG_EQUAL = (14,)
    EQUAL = (15,)
    EQUAL_EQUAL = (16,)
    GREATER = (17,)
    GREATER_EQUAL = (18,)
    LESS = (19,)
    LESS_EQUAL = (20,)
    RIGHT_ARROW = (21,)

    IDENTIFIER = (22,)
    STRING = (23,)
    FLOAT = (24,)
    INT = (100,)

    AND = (25,)
    ELSE = (26,)
    FALSE = (27,)
    FUNC = (28,)
    FOR = (29,)
    IF = (30,)
    NIL = (31,)
    OR = (32,)
    PRINT = (33,)
    RETURN = (34,)
    SUPER = (35,)
    THIS = (36,)
    TRUE = (37,)
    VAR = (38,)
    WHILE = 39

    TYPE_INT = (40,)
    TYPE_FLOAT = (41,)
    TYPE_STR = (42,)
    TYPE_BOOL = 43

    RIGHT_BRACK = (45,)
    LEFT_BRACK = 46

    @staticmethod
    def string_to_token_type(s: str):
        match s:
            # Tokens
            case "epsilon":
                return None
            case "EOF":
                return TokenType.EOF
            case "[":
                return TokenType.LEFT_BRACK
            case "]":
                return TokenType.RIGHT_BRACK
            case "(":
                return TokenType.LEFT_PAREN
            case ")":
                return TokenType.RIGHT_PAREN
            case "{":
                return TokenType.LEFT_BRACE
            case "}":
                return TokenType.RIGHT_BRACE
            case ",":
                return TokenType.COMMA
            case ".":
                return TokenType.DOT
            case "-":
                return TokenType.MINUS
            case "+":
                return TokenType.PLUS
            case ";":
                return TokenType.SEMICOLON
            case "/":
                return TokenType.SLASH
            case "*":
                return TokenType.STAR
            case "|":
                return TokenType.VERTICAL_BAR
            case "!":
                return TokenType.BANG
            case "!=":
                return TokenType.BANG_EQUAL
            case "=":
                return TokenType.EQUAL
            case "==":
                return TokenType.EQUAL_EQUAL
            case ">":
                return TokenType.GREATER
            case ">=":
                return TokenType.GREATER_EQUAL
            case "<":
                return TokenType.LESS
            case "<=":
                return TokenType.LESS_EQUAL
            case "->":
                return TokenType.RIGHT_ARROW
            case "IDENTIFIER":
                return TokenType.IDENTIFIER
            case "STRING":
                return TokenType.STRING
            case "INT":
                return TokenType.INT
            case "FLOAT":
                return TokenType.FLOAT
            case "AND":
                return TokenType.AND
            case "ELSE":
                return TokenType.ELSE
            case "FALSE":
                return TokenType.FALSE
            case "FUNCTION":
                return TokenType.FUNC
            case "FOR":
                return TokenType.FOR
            case "IF":
                return TokenType.IF
            case "NIL":
                return TokenType.NIL
            case "OR":
                return TokenType.OR
            case "PRINT":
                return TokenType.PRINT
            case "RETURN":
                return TokenType.RETURN
            case "SUPER":
                return TokenType.SUPER
            case "THIS":
                return TokenType.THIS
            case "TRUE":
                return TokenType.TRUE
            case "VAR":
                return TokenType.VAR
            case "WHILE":
                return TokenType.WHILE
            case "TYPE_INT":
                return TokenType.TYPE_INT
            case "TYPE_FLOAT":
                return TokenType.TYPE_FLOAT
            case "TYPE_STR":
                return TokenType.TYPE_STR
            case "TYPE_BOOL":
                return TokenType.TYPE_BOOL
            case _:
                return None

    @staticmethod
    def token_type_to_string(token_type: "TokenType") -> Optional[str]:
        match token_type:
            case TokenType.EOF:
                return "EOF"
            case TokenType.LEFT_BRACK:
                return "["
            case TokenType.RIGHT_BRACK:
                return "]"
            case TokenType.LEFT_PAREN:
                return "("
            case TokenType.RIGHT_PAREN:
                return ")"
            case TokenType.LEFT_BRACE:
                return "{"
            case TokenType.RIGHT_BRACE:
                return "}"
            case TokenType.COMMA:
                return ","
            case TokenType.DOT:
                return "."
            case TokenType.MINUS:
                return "-"
            case TokenType.PLUS:
                return "+"
            case TokenType.SEMICOLON:
                return ";"
            case TokenType.SLASH:
                return "/"
            case TokenType.STAR:
                return "*"
            case TokenType.VERTICAL_BAR:
                return "|"
            case TokenType.BANG:
                return "!"
            case TokenType.BANG_EQUAL:
                return "!="
            case TokenType.EQUAL:
                return "="
            case TokenType.EQUAL_EQUAL:
                return "=="
            case TokenType.GREATER:
                return ">"
            case TokenType.GREATER_EQUAL:
                return ">="
            case TokenType.LESS:
                return "<"
            case TokenType.LESS_EQUAL:
                return "<="
            case TokenType.IDENTIFIER:
                return "identifier"
            case TokenType.STRING:
                return "string"
            case TokenType.INT:
                return "int"
            case TokenType.FLOAT:
                return "float"
            case TokenType.AND:
                return "and"
            case TokenType.ELSE:
                return "else"
            case TokenType.FALSE:
                return "false"
            case TokenType.FUNC:
                return "function"
            case TokenType.FOR:
                return "for"
            case TokenType.IF:
                return "if"
            case TokenType.NIL:
                return "nil"
            case TokenType.OR:
                return "or"
            case TokenType.PRINT:
                return "print"
            case TokenType.RETURN:
                return "return"
            case TokenType.SUPER:
                return "super"
            case TokenType.THIS:
                return "this"
            case TokenType.TRUE:
                return "true"
            case TokenType.VAR:
                return "var"
            case TokenType.WHILE:
                return "while"
            case TokenType.TYPE_INT:
                return "type_int"
            case TokenType.TYPE_FLOAT:
                return "type_float"
            case TokenType.TYPE_STR:
                return "type_str"
            case TokenType.TYPE_BOOL:
                return "type_bool"
            case _:
                return None
