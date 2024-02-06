# Compiler Project - Team Blue
# Project goals
This project is about developing a compiler that has the LL(1) grammar and can be applied to the **ezC** language.
First, we build the front end of a compiler that contains a **lexical analyser**, a **syntactic analyser** and a **code generator** that is able to translate ezC into an intermediate representation (tbd). 

The parsers will be a **top-down, nonrecursive predictive Parser**.

The main programming language is **Python**.

### Project goals:
1. basics and principles of lexical analysis (scanning):
    - Description of the language to be lexemised 
    - Implementation of character classification and lexical token definition.

2. basics and principles of syntax analysis (parsing):
    - Description of the structure of the language (context-free grammar)
    - Implementation of syntax rules and syntax analysis strategies

3. architecture and modularity of lexer and parser:
    - Separation of lexical and syntactic analysis 
    - Merging the lexical and syntactic token streams 
    - Use of token buffers and lookahead functions to process conflicts and unusual structures 

4. examples and test scenarios:
    - Examples of valid and invalid input strings 
    - Description of test cases and expected values for the parser 

5. extension points and customisation options:
    - Possibility to extend lexical and syntactic grammar 
    - Possibility to customise lexical and syntactic rules for different programming languages





## The ezC Language
### 1. Specification
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
 
 ### 2. Grammar
 A valid ezC-program must follow the rules of the following **LL(1) grammar**:

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

## Lexical Analysis

### 1. Token-Types:
The following is a complete list of token-types our lexical analyzer recognizes. 
- EOF
- LEFT_PAREN, RIGHT_PAREN, LEFT_BRACE, RIGHT_BRACE, COMMA, DOT
- MINUS, PLUS, SEMICOLON, SLASH, STAR, VERTICAL_BAR
- BANG, BANG_EQUAL, EQUAL, EQUAL_EQUAL, GREATER, GREATER_EQUAL, LESS, LESS_EQUAL, RIGHT_ARROW
- IDENTIFIER, STRING, NUMBER
- AND, ELSE, FALSE, FUNC, IF, NIL, OR, PRINT, RETURN, SUPER, THIS, TRUE, VAR, WHILE


### 2. Implementation
Our lexical analyzer consists of a single class called `Lexer`. As one would expected of a lexical analyser, a lexer-object must be provided with a *filepath* and a *pointer to a symboltable*, upon initialization. When `generateTokens()` is called, the lexer will start going through the given file one character after another using **one lookahead** (LL(**1**)) and use some simple helper-functions to produce the correct tokens. Note, that longer tokens are always chosen over shorter tokens(e.g. `<=` over `<`).\
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

### Example
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

## Symboltable Stack
As suggested by the name, our compiler makes use of a stack of symboltables which are can, but do not have to, be connected with each other. This structure allows us to handle the simple block-scoping of the ezC language. 

### Functionality:
- Upon entering a new scope, a new symboltable is pushed ontop of the stack.
- The Symboltable of the scope that the program-state is in is always at the top of the stack.
- Upon leaving the current scope, the head(the corresponding symboltable) is poped off the stack.
- new entries can only be added to the head of the stack.
- When a new symboltable is pushed onto the stack, it must have a `parent-pointer`` to either one of the following two objects:
1. The Symboltable of the global scope. (end of stack)
2. The Symboltable that was at the head of the stack prior to then new scope. (the outer scope)
- The stack is initialised with an empty global symboltable as its root element. Therefore, the chain of parent-pointers of all future symboltables on the stack will lead to the global symboltable.
- When searching for an element, the head of the stack **and the chain of parent objects (outer scopes)**, up until the global symboltable, are being checked.

The following diagram shows our approach more clearly.

![](/docs/SymbolTableStack_Diagramm.png)

## Parsing Table
The parsin-table is generated by the equally named class `ParsingTable`. An object of this class is initialized with a hashtable. The hashtable must represent the grammar for which the table is to be constructed, where keys represent non-terminals and values represent their corresponding productions.

The following shows the expression grammar from the lecture, in 'hashtable-form'.\
Note, that EX and TX stand for E' and T'.
```python
grammarHash = {
    "E" : "T EX",
    "EX": "+ T EX|epsilon",
    "T" : "F TX",
    "TX": "* F TX|epsilon",
    "F" : "( E )|id"
}
```

### Functionality
The first and follow sets, and ultimately the parsing-table, are all constructed by the algorithms shown in the lecture.
The parsing-table is stored in a two-dimensional hashtable.

## Parser
The parsers works with an input-string, a stack, and the generated parsing-table, as shown in the lecture.

## Contributions to IR Generation
- Some Refactoring/Fixes:

- Implementation:
Peter

## Contributions
- **Project Management:**
Alexander
- **Project Setup and Structuring:**
Felix
- **Project Documentation:**
Nikolas, Friederike
- **Construction of ezC-Language:**
- **Construction of LL(1) ezC-Grammar:**
Peter
- **Implementation of Lexical Analyzer:**
Nikolas, Felix (refactoring)
- **Implementation of Parser:**
Martin, Wiktoria, Nikolas, Peter
- **Optimization**
Martin, Wiktoria
- **Writing tests:**
Felix, Friederike

