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

#-------------------------------
# TEMP VARIABLES
temp_count=0
all_temps=[]
def Temp(type):
    global temp_count, all_temps
    idx= temp_count
    temp_count += 1
    
    t= {
        "code": type+" t"+str(idx),
        "id": idx
    }
    all_temps.append(t)
    return t
    
# TEMP VARIABLES
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
    T = Label("Cond_True")
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
    start = Label("While_Start")
    
    node.children[2].true_label = T
    node.children[2].false_label= F
    
    node.managed_labels["True"]= T
    node.managed_labels["start"]= start
    # No need to manage F label
    
    node.children[4].next= start
    
def WHILESTMT_synth(node):
    expression = node.children[2]
    statement = node.children[5]
    node.code= f"{node.managed_labels['start']['code']} {expression.code} {node.managed_labels['True']['code']} {statement.code}"
    
def PRINTSTMT_inherit(node):
    expression= node.children[1]
    next=  Label("next")
    expression.next= next
    node.managed_labels["EXPR_next"]=next
    # Hope this is all
    
def PRINTSTMT_synth(node):
    expression= node.children[1]
    
    c_type_id = ""
    match expression.type:
        case "int":
            c_type_id= "%d"
        case "string":
            c_type_id= "%s"
        case "float":
            c_type_id= "%f"
    
    node.code= f'{expression.code} {node.managed_labels["EXPR_next"]["code"]} printf("{c_type_id}", {expression.res})'
    
def pass_on_TF_to_first_child(node):
    child= node.children[0]    
    if node.true_label:
        child.true_label= node.true_label
    if node.false_label:
        child.false_label= node.false_label

def EXPR_inherit(node):
    pass_on_TF_to_first_child(node)
    
def EXPR_bool_synth(node):
    elevel1 = node.children[0]
    exprx = node.children[1]
    operand = exprx.operand
    # type checking
    if exprx.type==None:
        node.type= elevel1.type
    elif exprx.type!= elevel1.type:
        print("TYPE ERROR")
        node.type= None
    else:
        node.type= elevel1.type

    if node.true_label and exprx.code:
        pass
    elif node.true_label:
        pass
    if exprx.code:
        node.res= Temp("bool")
        node.code = f' {elevel1.code} {exprx.code} {node.res["code"]} = {elevel1.res} {operand} {exprx.res};'
    else:
        node.res= elevel1.res
        node.code= f'{elevel1.code}'
        
def EXPR_number_synth(node):
    elevel1 = node.children[0]
    exprx = node.children[1]
    operand = exprx.operand
    # type checking
    if exprx.type==None:
        node.type= elevel1.type
    elif exprx.type!= elevel1.type:
        print("TYPE ERROR")
        node.type= None
    else:
        node.type= elevel1.type

    if node.true_label and exprx.code:
        pass
    elif node.true_label:
        pass
    if exprx.code:
        node.res= Temp(elevel1.type)
        node.code = f' {elevel1.code} {exprx.code} {node.res["code"]} = {elevel1.res} {operand} {exprx.code};'
    else:
        node.res= elevel1.res
        node.code= f'{elevel1.code}'
        
def EXPRX_synth(node):
    node.operand= node.children[0]
    expr = node.children[1]
    
    node.res = expr.res
    node.code = expr.code