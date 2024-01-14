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
    "DECLARATION": (inherit_next_2_children, synth_code_2_children)
  },
  "PROGRAMX": {
    "PROGRAM": (inherit_next_1_child, synth_code_1_child),
    "eof": "$$$$"
  },
  "DECLARATION": {
    "FUNCTIONDECL": (inherit_next_1_child, synth_code_1_child),
    "STATEMENT": (inherit_next_1_child, synth_code_1_child),
  },
  "TYPE": {
    "type_int": (get_and_inherit_base_type , synth_expected_type_and_width),
    "type_float": (get_and_inherit_base_type , synth_expected_type_and_width),
    "type_str": (get_and_inherit_base_type , synth_expected_type_and_width),
    "type_bool": (get_and_inherit_base_type , synth_expected_type_and_width),
  },
  "ARRAY":{
    "[": (inherit_base_type,synth_array),
    "epsilon": (stop_base_type_inheritance, None)
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
    "epsilon": "$$$$"
  },
  "ASSIGNMENT": {
    "TYPE": (None, None)
  },
  "EXPRSTMT": {
    "EXPRESSION": "$$$$"
  },
  "IFSTMT": {
    "if": "$$$$"
  },
  "IFSTMTX": {
    "else": "$$$$",
    "epsilon": "$$$$"
  },
  "PRINTSTMT": {
    "print": "$$$$"
  },
  "WHILESTMT": {
    "while": "$$$$"
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
    "ELEVEL1": "$$$$"
  },
  "EXPRESSIONX": {
    "or": "$$$$",
    "epsilon": "$$$$"
  },
  "ELEVEL1": {
    "ELEVEL2": "$$$$"
  },
  "ELEVEL1X": {
    "&&": "$$$$",
    "epsilon": "$$$$"
  },
  "ELEVEL2": {
    "ELEVEL3": "$$$$"
  },
  "ELEVEL2X": {
    "==": "$$$$",
    "epsilon": "$$$$"
  },
  "ELEVEL3": {
    "ELEVEL4": "$$$$"
  },
  "ELEVEL3X": {
    "COMPOPERATORS": "$$$$",
    "epsilon": "$$$$"
  },
  "ELEVEL4": {
    "ELEVEL5": "$$$$"
  },
  "ELEVEL4X": {
    "+": "$$$$",
    "-": "$$$$",
    "epsilon": "$$$$"
  },
  "ELEVEL5": {
    "ELEVEL6": "$$$$"
  },
  "ELEVEL5X": {
    "/": "$$$$",
    "*": "$$$$",
    "epsilon": "$$$$"
  },
  "ELEVEL6": {
    "!": "$$$$",
    "-": "$$$$",
    "ELEVEL6X": "$$$$"
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
