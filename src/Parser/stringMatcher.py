import sys
sys.path.append("../")

from TokenTypes import TokenType

class Matcher():
    @staticmethod
    def string_to_token_type(string):
        
        match string:
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
    def token_type_to_string(token_type):
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
                return "&&"
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
                return None  #