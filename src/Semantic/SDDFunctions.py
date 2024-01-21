"""
FILE SDD FUNCTIONS

WRITE NECESSARY FUNCTIONS FOR EACH PRODCUTION HERE

Include the function name in the appropriate place of the SDDHash

I think the functions should only take one node as input. This node is defined in Tree.py
"""

from src.Lexing.TokenTypes import TokenType

#-------------------------
# LABELS
number_of_labels= 0
all_labels=[]

def Label(name:str=""):
    global number_of_labels, all_labels
    idx = number_of_labels
    number_of_labels+=1
    l={
            "code": name+str(idx)+":",
            "name": name,
            "id":   idx
    }
    all_labels.append(l)
    return l

# LABELS
#-------------------------------
def inherit_next_2_children(Node):
    l = Label("next")
    Node.children[0].next = l
    Node.managed_labels["next"]=l
    Node.children[1].next= Node.next

def synth_code_2_children(Node):
    Node.code = Node.children[0].code +Node.managed_labels["next"]["code"]+ Node.children[1].code

def inherit_next_1_child(Node):
    Node.children[0].next=Node.next

def synth_code_1_child(Node):
    Node.code= Node.children[0].code

def synth_code_epsilon(Node):
    Node.code=""

def TYPE_synth_expected_type_and_width(Node):
        # get base type from type keyword
    token= TokenType.string_to_token_type(Node.children[0].label.upper())
    match token:
        case TokenType.TYPE_INT:
            Node.type= "int"
            Node.width= 16
        case TokenType.TYPE_FLOAT:
            Node.type= "float"
            Node.width= 32
        case TokenType.TYPE_STR:
            # in case of string we do not have any possible array
            Node.type= "str"
            return
        case TokenType.TYPE_BOOL:
            Node.type= "bool"
            Node.width= 16
        case __:
            raise SyntaxError("EXPECTED TYPE SPECIFIER")
    Node.code= Node.type
    
def TYPE_synth_type_from_Symbol_Table(Node):
    pass # TODO: Lookup previously declared value from symboltable

def inherit_next_to_last_child(Node):
    Node.children[len(Node.children)-1].next= Node.next

def ASSIGNMENT_synth(Node):
    # CHECK TYPE
    expected_type= Node.children[0].type
    actual_type= Node.children[3].type

    if expected_type!=actual_type:
        # TODO make Exception 
        print(f"TYPING ERROR: type {expected_type} does not match {actual_type}")
    else:
        Node.type=actual_type

    # SYNTH CODE
    Node.code= f"{Node.children[3].code} {Node.children[0].code} {Node.children[1].lexval} = {Node.children[3].res}; "
    
    # TODO:SYMBOL TABLE UPDATE
    #Node.symbol_table.add?
    
def EXPRSTMT_synth(Node):
    Node.type= Node.children[0].type
    Node.code= Node.children[0].code

def IFSTMT_inherit(Node):
    T,F = Label("Cond_True"),Label("Cond_False")
    Node.children[2].true_Label= T
    Node.children[2].false_Label= F
    Node.managed_labels["True"]= T
    Node.managed_labels["False"]=F
    
    true_next= Label("next")
    Node.children[4].next= true_next
    Node.managed_labels["True_next"]= true_next

    Node.children[5].next = Node.next

def IFSTMT_synth(Node):
    expression= Node.children[2]
    statement1= Node.children[4]
    statement2= Node.children[5]
    Node.code= f"{expression.code} {Node.managed_labels['True']['code']} {statement1.code} {Node.managed_labels['False']['code']} {statement2.code}"
    
def synth_code_from_last_child(Node):
    Node.code=Node.children[len(Node.children)-1].code
