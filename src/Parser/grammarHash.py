grammarHash = {
    "PROGRAM"           : "DECLARATION PROGRAMX",
    "PROGRAMX"          : "PROGRAM|eof",
    "DECLARATION"       : "FUNCTIONDECL|STATEMENT",

    "STATEMENT"         : "ASSIGNMENT STATEMENTX|IFSTMT STATEMENTX|PRINTSTMT STATEMENTX|WHILESTMT STATEMENTX|RETURNSTMT STATEMENTX",
    "STATEMENTX"         : "STATEMENT|epsilon",
    "ASSIGNMENT"        : "identifier = EXPRSTMT",
    "EXPRSTMT"          : "EXPRESSION ;",
    "IFSTMT"            : "if ( EXPRESSION ) BLOCK IFSTMTX",
    "IFSTMTX"           : "else BLOCK|epsilon",
    "PRINTSTMT"         : "print EXPRESSION ;",
    "WHILESTMT"         : "while ( EXPRESSION ) { STATEMENT }",
    "RETURNSTMT"        : "return EXPRESSION ;",
    "BLOCK"             : "{ STATEMENT }",

    "FUNCTIONDECL"      : "function identifier ( PARAMETERS ) BLOCK",
    "PARAMETERS"        : "epsilon|identifier PARAMETERSX",
    "PARAMETERSX"       : "epsilon|, identifier PARAMETERSX",
    "ARGUMENTS"         : "EXPRESSION ARGUMENTSX",
    "ARGUMENTSX"        : ", EXPRESSION ARGUMENTSX|epsilon",

    "EXPRESSION"        : "ELEVEL1 EXPRESSIONX",
    "EXPRESSIONX"       : "or EXPRESSION|epsilon",
    "ELEVEL1"           : "ELEVEL2 ELEVEL1X",
    "ELEVEL1X"          : "&& ELEVEL1|epsilon",
    "ELEVEL2"           : "ELEVEL3 ELEVEL2X",
    "ELEVEL2X"          : "== ELEVEL2|epsilon",
    "ELEVEL3"           : "ELEVEL4 ELEVEL3X",
    "ELEVEL3X"          : "COMPOPERATORS ELEVEL4|epsilon",
    "ELEVEL4"           : "ELEVEL5 ELEVEL4X",
    "ELEVEL4X"          : "+ ELEVEL4|- ELEVEL4|epsilon",
    "ELEVEL5"           : "ELEVEL6 ELEVEL5X",
    "ELEVEL5X"          : "/ ELEVEL5|* ELEVEL5|epsilon",
    "ELEVEL6"           : "! ELEVEL6X|- ELEVEL6X|ELEVEL6X",
    "ELEVEL6X"          : "PRIMARY|FUNCCALLORVARIABLE",
    "PRIMARY"           : "true|false|nil|number|string|( EXPRESSION )",
    "FUNCCALLORVARIABLE": "identifier FUNCCALLX",
    "FUNCCALLX"         : "( ARGUMENTS )|epsilon",
    "COMPOPERATORS"     : "<=|<|>|>=|!="
 }

'''
grammarHash = {
    "E": "T EX",
    "EX": "+ T EX|epsilon",
    "T": "F TX",
    "TX": "* F TX|epsilon",
    "F": "( E )|identifier"
}
'''