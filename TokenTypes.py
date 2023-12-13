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
    NUMBER        = 24,

    AND           = 25,
    CLASS         = 26,
    ELSE          = 27,
    FALSE         = 28,
    FUNC          = 29,
    FOR           = 30,
    IF            = 31,
    NIL           = 32,
    OR            = 33,
    PRINT         = 34,
    RETURN        = 35,
    SUPER         = 36,
    THIS          = 37,
    TRUE          = 38,
    VAR           = 39,
    WHILE         = 40