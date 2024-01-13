from enum import Enum

class TokenType(Enum):
    EOF           = 0,

    LEFT_PAREN    = 1, 
    RIGHT_PAREN   = 2, 
    LEFT_BRACE    = 3, 
    RIGHT_BRACE   = 4,
    COMMA         = 5, 
    DOT           = 6, 
    MINUS         = 7,
    PLUS          = 8, 
    SEMICOLON     = 9, 
    SLASH         = 10, 
    STAR          = 11,
    VERTICAL_BAR  = 12,

    BANG          = 13,
    BANG_EQUAL    = 14,
    EQUAL         = 15,
    EQUAL_EQUAL   = 16,
    GREATER       = 17,
    GREATER_EQUAL = 18,
    LESS          = 19,
    LESS_EQUAL    = 20,
    RIGHT_ARROW   = 21,

    IDENTIFIER    = 22,
    STRING        = 23,
    FLOAT         = 24,
    INT           = 100,

    AND           = 25,
    ELSE          = 26,
    FALSE         = 27,
    FUNC          = 28,
    FOR           = 29,
    IF            = 30,
    NIL           = 31,
    OR            = 32,
    PRINT         = 33,
    RETURN        = 34,
    SUPER         = 35,
    THIS          = 36,
    TRUE          = 37,
    VAR           = 38,
    WHILE         = 39

    TYPE_INT      =40,
    TYPE_FLOAT    =41,
    TYPE_STR      =42,
    TYPE_BOOL     =43