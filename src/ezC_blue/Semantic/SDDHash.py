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
    "return": "$$$$"
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
    "EXPRESSION": "$$$$"
  },
  "ARGUMENTSX": {
    ",": "$$$$",
    "epsilon": "$$$$"
  },
  "EXPRESSION": {
    "ELEVEL1": (EXPR_inherit, EXPR_bool_synth)
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
    "ELEVEL3": (None, synth_code_epsilon)
  },
  "ELEVEL2X": {
    "==": "$$$$",
    "epsilon": (None, synth_code_epsilon)
  },
  "ELEVEL3": {
    "ELEVEL4": "$$$$"
  },
  "ELEVEL3X": {
    "COMPOPERATORS": "$$$$",
    "epsilon": (None, synth_code_epsilon)
  },
  "ELEVEL4": {
    "ELEVEL5": "$$$$"
  },
  "ELEVEL4X": {
    "+": "$$$$",
    "-": "$$$$",
    "epsilon": (None, synth_code_epsilon)
  },
  "ELEVEL5": {
    "ELEVEL6": "$$$$"
  },
  "ELEVEL5X": {
    "/": "$$$$",
    "*": "$$$$",
    "epsilon": (None, synth_code_epsilon)
  },
  "ELEVEL6": {
    "!": "$$$$",
    "-": "$$$$",
    "ELEVEL6X": (None, synth_code_epsilon)
  },
  "ELEVEL6X": {
    "PRIMARY": "$$$$",
    "FUNCCALLORVARIABLE": "$$$$"
  },
  "PRIMARY": {
    "true": "$$$$",
    "false": "$$$$",
    "nil": "$$$$",
    "float": "$$$$",
    "int": "$$$$",
    "string": "$$$$",
    "(": "$$$$"
  },
  "FUNCCALLORVARIABLE": {
    "identifier": "$$$$"
  },
  "FUNCCALLX": {
    "(": "$$$$",
    "epsilon": "$$$$"
  },
  "COMPOPERATORS": {
    "<=": "$$$$",
    "<": "$$$$",
    ">": "$$$$",
    ">=": "$$$$",
    "!=": "$$$$"
  }
}
