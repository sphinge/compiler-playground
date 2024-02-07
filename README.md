# Compiler Project - Team Blue
# Project goals
This project is about developing a compiler that has the LL(1) grammar and can be applied to the **ezC** language.
First, we build the front end of a compiler that contains a **lexical analyser**, a **syntactic analyser** and a **code generator** that is able to translate ezC into an intermediate representation (tbd). 

The parsers will be a **top-down, nonrecursive predictive Parser**.

The main programming language is **Python**.



## The ezC Language
### 0. Specification
ezC has basic functionality, including:\
\
**- Floating-Points:** `10.0`\
**- Strings:** `"Hi, my name is"`\
**- Boolean-Values:** `true, false`\
**- Null-Values:** `Nil`\
**- Typeless Variables:** `name = "John"`\
**- Functions:** `calculateBMI(height, weight){... return bmi}`\
**- Blocks:** `{...}`\
**- Conditional Statements:** `if{...} else{...}` where `else` is optional\
**- Operators:**
- mathematical: +, -, *, /, =, <, >, <=, >=, !=
- logical: !, ==, &&, || \

**- While-Loops:** `while(condition){...}`\
 

### Project:
## 1. basics and principles of lexical analysis (scanning):
    - Description of the language to be lexemised 
    A simple grammar in BNF notation is defined in the grammarHash.py file. The hash table represents the grammar rules of the language. 
    Example: The production "EXPRESSION" contains definitions of subordinate expressions such as "ELEVEL1" and "EXPRESSIONX"
    A valid ezC programme must follow the rules of the flying LL(1) grammar:


>### Productions
>starting NT: program\
>program        → declaration program'\
>program'       → program | _EOF_\
>declaration    → functionDecl
>               | statement
>
>### Statements
>statement      → assignment
>                | ifStmt
>                | printStmt
>                | whileStmt
>                | returnStmt\
>assignment     → _IDENTIFIER_ _=_ exprStmt\
>exprStmt       → expression _;_\
>ifStmt         → _if_ _(_ expression _)_ block ifStmt\
>ifStmt'        →  _else_ block | _epsilon_\
>printStmt      → _print_ expression _;_\
>whileStmt      → _while_ _(_ expression _)_ _{_ statement _}_\
>returnStmt     → _return_ expression _;_\
>block          → _{_ statement _}_
>
>### Functions
>functionDecl   → _function_ _ID_ _(_ parameters _)_ block\
>parameters     →  _epsilon_ | _IDENTIFIER_ parameters'\
>parameters'    → _epsilon_| , _IDENTIFIER_ parameters'\
>arguments      → expression arguments'\
>arguments'     → , arguments' | epsilon\
>
>### Expressions
>expression → e_level1 expression'\
>expression' → || expression | _epsilon_\
>e_level1    → e_level2 e_level1'\
>e_level1'   → && e_level1 | _epsilon_\
>e_level2    → e_level3 e_level2'\
>e_level2'   →  _==_ e_level2 | _epsilon_\
>e_level3    → e_level4 e_level3'\
>e_level3'   → comp_operators e_level4 | _epsilon_\
>e_level4    → e_level5 e_level4'\
>e_level4'   → _+_ e_level4 | _-_ e_level4 | _epsilon_\
>e_level5    → e_level6 e_level5'\
>e_level5'   → _/_ e_level5 | _*_ e_level5 | _epsilon_\
>e_level6    → _!_ e_level6' | - e_level6' | e_level6'  // introduces ambigouity \
>e_level6'   → primary | funcCall_or_variable\
>primary     → _true_ | _false_ | _NIL_ | _NUMBER_ | _STRING_ | _(_ expression _)_\
>funcCall_or_variable → _IDENTIFIER_ (funcCall')\
>funcCall'   → (arguments) | _epsilon_\
>comp_operators → <= | < | > | >= | !=  // is determined by lexer, < and <= are atomic tokens


- The file TokenTyps.py contains a TokenType enumeration for the lexer. The code has two static 
  methods for converting between string representations and enum values. 
- Below is a complete list of the token types that our lexical analyser recognises.

- EOF
- LEFT_PAREN, RIGHT_PAREN, LEFT_BRACE, RIGHT_BRACE, COMMA, DOT
- MINUS, PLUS, SEMICOLON, SLASH, STAR, VERTICAL_BAR
- BANG, BANG_EQUAL, EQUAL, EQUAL_EQUAL, GREATER, GREATER_EQUAL, LESS, LESS_EQUAL, RIGHT_ARROW
- IDENTIFIER, STRING, NUMBER
- AND, ELSE, FALSE, FUNC, IF, NIL, OR, PRINT, RETURN, SUPER, THIS, TRUE, VAR, WHILE

- The lexer.py file analyses and breaks down the source code into a list of tokens. 
  The Lexer class contains attributes, methods and a token recogniser. 
    
    Example:The "handleString" method processes character strings (text,
    enclosed in inverted commas) from a source code.
    If the lexer encounters an opening inverted comma ("), this method is called.
    It reads characters until it encounters the closing inverted commas (") and adds them to a token.
    If no closing inverted commas are found or a new line is contained in the string
    an error message is displayed ("missing closing asterix").

- Implementation of character classification and lexical token definition.

This lexical analyzer consists of a single class called `Lexer`. As one would expected of a lexical analyser, a lexer-object must be provided with a *filepath* and a *pointer to a symboltable*, upon initialization. When `generateTokens()` is called, the lexer will start going through the given file one character after another using **one lookahead** (LL(**1**)) and use some simple helper-functions to produce the correct tokens. Note, that longer tokens are always chosen over shorter tokens(e.g. `<=` over `<`).\
The following code shows the overall matching process, where `self.peek` returns the character the lexer is currently scanning.


```python
def scanTokens(self):
        while not self.reachedEnd():
            match self.peek():
                case '(': self.consumeToken(TokenType.LEFT_PAREN)
                case ')': self.consumeToken(TokenType.RIGHT_PAREN)
                case '{': self.consumeToken(TokenType.LEFT_BRACE)
                case '}': self.consumeToken(TokenType.RIGHT_BRACE)
                case ',': self.consumeToken(TokenType.COMMA)
                case '.': self.consumeToken(TokenType.DOT)
                case '-': self.consumeToken(TokenType.MINUS)
                case '+': self.consumeToken(TokenType.PLUS)
                case ';': self.consumeToken(TokenType.SEMICOLON)
                case '*': self.consumeToken(TokenType.STAR)
                case '!': self.consumeToken(TokenType.BANG_EQUAL) if self.isFollowedBy('=') else self.consumeToken(TokenType.BANG)
                case '=': self.consumeToken(TokenType.EQUAL_EQUAL) if self.isFollowedBy('=') else self.consumeToken(TokenType.EQUAL)
                case '<': self.consumeToken(TokenType.LESS_EQUAL) if self.isFollowedBy('=') else self.consumeToken(TokenType.LESS)
                case '>': self.consumeToken(TokenType.GREATER_EQUAL) if self.isFollowedBy('=') else self.consumeToken(TokenType.GREATER)
                case '/': self.consumeToken(TokenType.SLASH) if self.lookahead() != '/' else self.skipComment()
                case " ": self.moveToNextLexeme()
                case '\r': self.moveToNextLexeme()
                case '\t': self.moveToNextLexeme()
                case '\n': self.moveToNextLexeme()
                case '"': self.handleString()
                case __: 
                    if self.isDigit(self.peek()): 
                        self.handleNumber()
                    elif self.isAlpha(self.peek()):
                        self.handleIdentifier()
                    else:
                        print(self.currentLine, "unexpected character.")
                        self.moveToNextLexeme()
```
The compiler uses a stack of symbol tables, which may or may not be linked together. This structure allows us to handle the simple block scoping of the ezC language.
Functionality:
    - When entering a new area, a new symbol table is placed on the stack. 
    - The symbol table of the area in which the programme status is located is always at the top of the stack. 
    - When leaving the current area, the header (the corresponding symbol table) is removed from the stack. 
    - New entries can only be added at the top of the stack. 
    - If a new symbol table is moved to the stack, it must have a "parent pointer" to one of the following two objects: 
    1. the symbol table of the global area. (end of the stack) 
    2. the symbol table that was at the top of the stack before the new scope. (the outer area) 
    - The stack is initialised with an empty global symbol table as the root element. Therefore, the chain of parent pointers of all future symbol tables on the stack leads to the global symbol table. 
    - When searching for an element, the header of the stack and the chain of higher-level objects (outer areas) are checked up to the global symbol table.
The following diagram shows this approach more clearly. [](/docs/SymbolTableStack_Diagramm.png)


### Example for the lexer
As an Example, when the following text is provided:\
>2;\
"Hello World"\
32345.123\
(){};\
var i <=23;\
var j =(i +1) * 2; // alksdjhfkj<<<=>//()\

the following list of tokens will be generated by the lexer:
```python
[
    [TokenType.SEMICOLON.name, None],
    [TokenType.NUMBER.name, 2.0],
    [TokenType.SEMICOLON.name, None],
    [TokenType.STRING.name, "Hello World"],
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
```


## 2. basics and principles of syntax analysis (parsing):
- Description of the structure of the language (context-free grammar)
The grammar LL(1) is represented in the hash table, with keys, non-terminals and values representing their corresponding productions. 
The parsin-table is generated by the equally named class `ParsingTable`. An object of this class is initialised with a hash table.     
In the following, the expression grammar from the lecture is shown in "hashtable form". 
Note that EX and TX stand for E' and T'.

```python
grammarHash = {
    "E" : "T EX",
    "EX": "+ T EX|epsilon",
    "T" : "F TX",
    "TX": "* F TX|epsilon",
    "F" : "( E )|id"
}
```
The Parser.py file is used for error handling, e.g. triggering exceptions if an unexpected token or invalid production occurs.
This code has a modular structure and contains the syntactic analysis of inputs in a specific format.

    - Implementation of syntax rules and syntax analysis strategies
Functionality for the first and follow sets, and ultimately the parsing-table, are all constructed by the algorithms shown in the lecture.
The parsing-table is stored in a two-dimensional hashtable and the Parser.py file is used for error handling, e.g. triggering exceptions if an unexpected token or invalid production occurs.
This code has a modular structure and contains the syntactic analysis of inputs in a specific format.

The intermediate representation is is 3AC-like C.

We use the parse tree to calculate synthesized and inherited attributes of each production.
For this we have functions that represent Syntax directed definitions. (SDDfunctions.py)
For more detailed info, see Issue ezc/bluecompiler#15



## 3. architecture and modularity of lexer and parser:
    - Separation of lexical and syntactic analysis 
    - Merging the lexical and syntactic token streams ( Block-Scoping, Lookahead LL(1))
    - Use of token buffers and lookahead functions to process conflicts and unusual structures 

## 4. examples and test scenarios:
    - Examples of valid and invalid input strings 
    - Description of test cases and expected values for the parser 

## 5. extension points and customisation options:
    - Possibility to extend lexical and syntactic grammar 
  (5)-> Improvement(lexer): Adapt specifications to language and case-sensitivity requirements. 

    - Possibility to customise lexical and syntactic rules for different programming languages








## Contributions
- **Project Management:**
Alexander
- **Project Setup and Structuring:**
Martin,Felix
- **Project Documentation:**
Nikolas, Friederike
- **Construction of ezC-Language:**
- **Construction of LL(1) ezC-Grammar:**
Peter
- **Implementation of Lexical Analyzer:**
Nikolas, Felix (refactoring)
- **Implementation of Parser:**
Martin, Wiktoria, Nikolas, Peter
- **Intermediate Representation Generation**
Peter
- **Optimization**
Martin, Wiktoria
- **Writing tests:**
Felix, Friederike

