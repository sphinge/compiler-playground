"""
FILE SDDHash

The SDD Hash contains exactly one (leaf) entry per production (NonTerminal != production !!!)

The $$$$ string is a placeholer. For every production, we need to write 2 functions.
This function represents the SDD of that production.
This function will be registered to each production in the Parse tree. 
We then do a postorder traversal of the Parsetree and call this function for each element.

One function will be executed before looking at the children of the node in question, 
the other will be executed after looking at all the cildren

The function should handle: 

- Evaluation of static values
- Typechecking
- Code Generation

For this we need to set multiple variables for each node. for example, each node that is descendant from a 
expression node should have a type and probably a value.

To be expanded, as i do not understand SDD fully myself :(

Code generation
"""
from Semantic.SDDFunctions import *

SDDHash = {
  "PROGRAM": {
    "DECLARATION":  (inherit_next_2_children, synth_code_2_children)
  },
  "PROGRAMX": {
    "PROGRAM":      (inherit_next_1_child, synth_code_1_child),
    "EOF":          (None, synth_code_epsilon)
  },
  "DECLARATION": {
    "FUNCTIONDECL": (inherit_next_1_child, synth_code_1_child),
    "STATEMENT":    (inherit_next_1_child, synth_code_1_child),
  },
  "TYPE": {
    "type_int":     (None, TYPE_synth_expected_type_and_width),
    "type_float":   (None, TYPE_synth_expected_type_and_width),
    "type_str":     (None, TYPE_synth_expected_type_and_width),
    "type_bool":    (None, TYPE_synth_expected_type_and_width),
  },
  "STATEMENT": {
    "ASSIGNMENT": (inherit_next_2_children, synth_code_2_children),
    "IFSTMT": (inherit_next_2_children, synth_code_2_children),
    "PRINTSTMT": (inherit_next_2_children, synth_code_2_children),
    "WHILESTMT": (inherit_next_2_children, synth_code_2_children),
    "RETURNSTMT": (inherit_next_2_children, synth_code_2_children)
  },
  "STATEMENTX": {
    "STATEMENT": (inherit_next_1_child, synth_code_1_child),
    "epsilon": (None, synth_code_epsilon)
  },
  "ASSIGNMENT": {
    "TYPE": (inherit_next_to_last_child, ASSIGNMENT_synth)
  },
  "EXPRSTMT": {
    "EXPRESSION": (inherit_next_1_child, EXPRSTMT_synth)
  },
  "IFSTMT": {
    "if": (IFSTMT_inherit, IFSTMT_synth)
  },
  "IFSTMTX": {
    "else": (inherit_next_to_last_child, synth_code_from_last_child),
    "epsilon": (None, synth_code_epsilon)
  },
  "PRINTSTMT": {
    "print": (PRINTSTMT_inherit, PRINTSTMT_synth)
  },
  "WHILESTMT": {
    "while": (WHILESTMT_inherit, WHILESTMT_synth)
  },
  "RETURNSTMT": {
    "return": (RETSTMT_inherit, RETSTMT_synth)
  },
  "BLOCK": {
    "{": "$$$$"
  },
  "FUNCTIONDECL": {
    "function": "$$$$"
  },
  "PARAMETERS": {
    "epsilon": "$$$$",
    "identifier": "$$$$"
  },
  "PARAMETERSX": {
    "epsilon": "$$$$",
    ",": "$$$$"
  },
  "ARGUMENTS": {
    "EXPRESSION": (None, ARGS_synth)
  },
  "ARGUMENTSX": {
    ",": (None, ARGSX_synth),
    "epsilon": (None, synth_code_epsilon)
  },
  "EXPRESSION": {
    "ELEVEL1": (EXPR_inherit, EXPR_bool_highest_add_gotos)
  },
  "EXPRESSIONX": {
    "or": (EXPR_inherit, EXPRX_synth),
    "epsilon": (None, synth_code_epsilon)
  },
  "ELEVEL1": {
    "ELEVEL2":(EXPR_inherit, EXPR_bool_synth)
  },
  "ELEVEL1X": {
    "and":(EXPR_inherit, EXPRX_synth),
    "epsilon":(None, synth_code_epsilon)
  },
  "ELEVEL2": {
    "ELEVEL3":  (EXPR_inherit, EXPR_bool_synth)
  },
  "ELEVEL2X": {
    "==": (EXPR_inherit, EXPRX_synth),
    "epsilon": (None, synth_code_epsilon)
  },
  "ELEVEL3": {
    "ELEVEL4":  (EXPR_inherit, EXPR_bool_synth)
  },
  "ELEVEL3X": {
    "COMPOPERATORS": (None,EXPRX3_synth),
    "epsilon": (None, synth_code_epsilon)
  },
  "ELEVEL4": {
    "ELEVEL5":  (EXPR_inherit, EXPR_number_synth)
  },
  "ELEVEL4X": {
    "+": (EXPR_inherit, EXPRX_synth),
    "-": (EXPR_inherit, EXPRX_synth),
    "epsilon": (None, synth_code_epsilon)
  },
  "ELEVEL5": {
    "ELEVEL6": (EXPR_inherit, EXPR_number_synth)
  },
  "ELEVEL5X": {
    "/": (EXPR_inherit, EXPRX_synth),
    "*": (EXPR_inherit, EXPRX_synth),
    "epsilon": (None, synth_code_epsilon)
  },
  "ELEVEL6": {
    "!": (EXPR_inherit, EXPR_invert_synth),
    "-": (EXPR_inherit, EXPR_invert_synth),
    "ELEVEL6X": (EXPR_inherit, EXPR_L6_synth),
  },
  "ELEVEL6X": {
    "PRIMARY": (EXPR_inherit, EXPR_PRIMARY_synth),
    "FUNCCALLORVARIABLE": (EXPR_inherit, EXPR_identifier_synth)
  },
  "PRIMARY": {
    "true": (EXPR_inherit, EXPR_PRIMARY_getValue_synth),
    "false": (EXPR_inherit, EXPR_PRIMARY_getValue_synth),
    "nil": "$$$$",#(EXPR_inherit, EXPR_PRIMARY_getValue_synth),
    "float": (EXPR_inherit, EXPR_PRIMARY_getValue_synth),
    "int": (EXPR_inherit, EXPR_PRIMARY_getValue_synth),
    "string": (EXPR_inherit, EXPR_PRIMARY_getValue_synth),
    "(": "$$$$"
  },
  "FUNCCALLORVARIABLE": {
    "identifier": (EXPR_inherit, VARORCALL_synth)
  },
  "FUNCCALLX": {
    "(": (None, FUNCX_synth),
    "epsilon": (None, synth_code_epsilon)
  },
  "COMPOPERATORS": {
    "<=": (None,COMPOP_synth),
    "<": (None,COMPOP_synth),
    ">": (None,COMPOP_synth),
    ">=": (None,COMPOP_synth),
    "!=": (None,COMPOP_synth),
  }
}
