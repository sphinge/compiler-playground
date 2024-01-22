"""
FILE SDD FUNCTIONS

WRITE NECESSARY FUNCTIONS FOR EACH PRODCUTION HERE

Include the function name in the appropriate place of the SDDHash

I think the functions should only take one node as input. This node is defined in Tree.py
"""

from Lexing.TokenTypes import TokenType

#-------------------------
# LABELS
number_of_labels = 0
all_labels = []

def Label(name:str = ""):
    global number_of_labels, all_labels
    idx = number_of_labels
    number_of_labels += 1

    l = {
            "code": name + str(idx) + ":",
            "name": name,
            "id":   idx
    }

    all_labels.append(l)
    return l

# LABELS
#-------------------------------
def inherit_next_2_children(node):
    l = Label("next")
    node.children[0].next = l
    node.managed_labels["next"] = l
    node.children[1].next = node.next

def synth_code_2_children(node):
    node.code = node.children[0].code + node.managed_labels["next"]["code"] + node.children[1].code

def inherit_next_1_child(node):
    node.children[0].next = node.next

def synth_code_1_child(node):
    node.code = node.children[0].code

def synth_code_epsilon(node):
    node.code = ""

def TYPE_synth_expected_type_and_width(node):
    # get base type from type keyword
    token= TokenType.string_to_token_type(node.children[0].label.upper())

    match token:
        case TokenType.TYPE_INT:
            node.type= "int"
            node.width= 16
        case TokenType.TYPE_FLOAT:
            node.type= "float"
            node.width= 32
        case TokenType.TYPE_STR:  # in case of string we do not have any possible array
            node.type= "string"
            node.width= None
        case TokenType.TYPE_BOOL:
            node.type= "bool"
            node.width= 16
        case __:
            raise SyntaxError("EXPECTED TYPE SPECIFIER")
        
    node.code= node.type
    
def TYPE_synth_type_from_Symbol_Table(node):
    pass # TODO: Lookup previously declared value from symboltable

def inherit_next_to_last_child(node):
    node.children[len(node.children)-1].next = node.next

def ASSIGNMENT_synth(node):
    # CHECK TYPE
    expected_type = node.children[0].type
    actual_type = node.children[3].type

    if expected_type != actual_type:
        # TODO make Exception 
        print(f"TYPING ERROR: type {expected_type} does not match {actual_type}")
    else:
        node.type = actual_type

    # SYNTH CODE
    node.code = f"{node.children[3].code} {node.children[0].code} {node.children[1].lexval} = {node.children[3].res}; "
    
    # TODO:SYMBOL TABLE UPDATE
    #node.symbol_table.add?
    
def EXPRSTMT_synth(node):
    node.type = node.children[0].type
    node.code = node.children[0].code

def IFSTMT_inherit(node):
    T= Label("Cond_True"),
    F = Label("Cond_False")

    node.children[2].true_Label  = T
    node.children[2].false_Label = F
    node.managed_labels["True"]  = T
    node.managed_labels["False"] = F
    
    true_next = Label("next")
    node.children[4].next = true_next
    node.managed_labels["True_next"] = true_next

    node.children[5].next = node.next

def IFSTMT_synth(node):
    expression = node.children[2]
    statement1 = node.children[4]
    statement2 = node.children[5]
    node.code = f"{expression.code} {node.managed_labels['True']['code']} {statement1.code} {node.managed_labels['False']['code']} {statement2.code}"
    
def synth_code_from_last_child(node):
    node.code = node.children[len(node.children)-1].code

def WHILESTMT_inherit(node):
    T = Label("Cond_True")
    F= node.next
    
    node.children[1]