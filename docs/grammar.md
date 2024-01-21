# Grammar for Parser

## **leftfactored & Left recursion free  Grammar**

### Productions

starting NT: program

program        → declaration program'

program'        -> program | _EOF_

declaration    → functionDecl
               | statement

### Statements

type           → __int__ | __string__ | __float__ | __bool__

statement      → assignment
                | ifStmt
                | printStmt
                | whileStmt
                | returnStmt

assignment     → type _IDENTIFIER_ _=_ exprStmt // causes ambigouity

exprStmt       → expression _;_

ifStmt         → _if_ _(_ expression _)_ block ifStmt'

ifStmt'        ->  _else_ block | _epsilon_


printStmt      → _print_ expression _;_

whileStmt      → _while_ _(_ expression _)_ _{_ statement _}_

returnStmt     → _return_ expression _;_

block          → _{_ statement _}_

### Functions

functionDecl   → _function_ tyoe _ID_ _(_ parameters _)_ block

parameters     →  _epsilon_ | _IDENTIFIER_ parameters'

parameters'    -> _epsilon_| , _IDENTIFIER_ parameters'

arguments      → expression arguments'

arguments'     -> , arguments' | epsilon

### Expressions

// I hope this works because i have no idea how to validate it

expression → e_level1 expression'

expression' → || expression | _epsilon_

e_level1    → e_level2 e_level1'

e_level1'   → && e_level1 | _epsilon_

e_level2    → e_level3 e_level2'

e_level2'   →  _==_ e_level2 | _epsilon_

e_level3    → e_level4 e_level3'

e_level3'   → comp_operators e_level4 | _epsilon_ // no definition for 3\< 3\< 3 so no recursion 

e_level4    → e_level5 e_level4'

e_level4'   → _+_ e_level4 | _-_ e_level4 | _epsilon_

e_level5    → e_level6 e_level5'

e_level5'   → _/_ e_level5 | _*_ e_level5 | _epsilon_

e_level6    → _!_ e_level6' | - e_level6' | e_level6'  // introduces ambigouity

e_level6'   → primary | funcCall_or_variable

primary     → _true_ | _false_ | _NIL_ | _NUMBER_ | _STRING_ | _(_ expression _)_

funcCall_or_variable → _IDENTIFIER_ (funcCall')

funcCall'   → (arguments) | _epsilon_

c
omp_operators → <= | < | > | >= | !=  // is determined by lexer, < and <= are atomic tokens


## First and Follow Sets

|NT | FIRST | FOLLOW|
|--|--|--|
|program | FIRST(declaration)| FIRST(program')
|program’| FIRST(program)+ EOF | FIRST(program)+ $|
| declaration | {function}+FIRST(statement)| FIRST(program)+EOF
| statement | {_IDENTIFIER_, if , print, while, return} | { _}_ , EOF, FIRST(program)}|
| assignment | {_IDENTIFIER_} | FOLLOW(statement)|
| exprStmt | FIRST(expression) | FOLLOW(assignment)|
| ifStmt | if | FOLLOW(statement)|
| printStmt | print | FOLLOW(statement)|
| whileStmt | while | FOLLOW(statement)|
| returnStmt | return | FOLLOW(statement)|
| block |  { | FOLLOW(statement)+ FOLLOW(functionDecl)
| functionDecl | function | FIRST(declaration)|
| parameters | epsilon, _IDENTIFIER_| )|
| parameters' | epsilon , __,__ | )|
| arguments | FIRST(expression) | ) |
| arguments'| , , epsilon | )|
| | |
| expression | FIRST(e_level1) | \{ __;__ , __)__ \}
| expression' | __OR__ , epsilon |  \{ __;__ , __)__ \}
| e_level1 | FIRST(e_level2) | \{ __;__ , __)__ , __OR__ \}
| e_level1' | __AND__ , epsilon |  \{ __;__ , __)__ , __OR__ \}
| e_level2 | FIRST(e_level3)|  \{ __;__ , __)__ , __OR__ ,__AND__\}
| e_level2' | __==__ , epsilon |  \{ __;__ , __)__ , __OR__, __AND__ \}
| e_level3 | FIRST(e_level4) |  \{ __;__ , __)__ , __OR__, __AND__ \}|
| e_level3' | FIRST(comp_operators) |  \{ __;__ , __)__ , __OR__, __AND__ \}
| e_level4 | FIRST(e_level5) |  \{ __;__ , __)__ , __OR__, __AND__\} + FIRST(comp_operators)
| e_level4' | +,-, epsilon |  \{ __;__ , __)__ , __OR__, __AND__\} + FIRST(comp_operators) |
| e_level5 | FIRST(e_level6) | \{ __;__ , __)__ , __OR__, __AND__ , + ,-\} + FIRST(comp_operators) |
| e_level5' | *, / , epsilon | \{ __;__ , __)__ , __OR__, __AND__, +, - \} + FIRST(comp_operators)|
| e_level6| - + FIRST(e_level6' ) | \{ __;__ , __)__ , __OR__, __AND__, +, - \} + FIRST(comp_operators)|
| e_level6' | FIRST(primary) + FIRST(funcCall_or_variable) | \{ __;__ , __)__ , __OR__, __AND__, +, - \} + FIRST(comp_operators)|
| primary| \{ true, false, NIL, NUMBER, STRING, (\} | \{ __;__ , __)__ , __OR__, __AND__, +, - \} + FIRST(comp_operators)|
| funcCall_or_variable | _IDENTIFIER_ | \{ __;__ , __)__ , __OR__, __AND__, +, - \} + FIRST(comp_operators)|
funcCall' | ( , epsilon | \{ __;__ , __)__ , __OR__, __AND__, +, - \} + FIRST(comp_operators) |
| comp_operators | < , > , ! | FIRST(e_level4) |
|comp' | = , epsilon | FIRST(e_level4) |
