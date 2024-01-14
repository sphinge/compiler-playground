"""
FILE SDD FUNCTIONS

WRITE NECESSARY FUNCTIONS FOR EACH PRODCUTION HERE

Include the function name in the appropriate place of the SDDHash

I think the functions should only take one node as input. This node is defined in Tree.py
"""

from TokenTypes import TokenType


#-------------------------
# LABELS
number_of_labels= 0
all_labels=[]

def Label(name:str=""):
    global number_of_labels, all_labels
    idx = number_of_labels
    number_of_labels+=1
    l={
            "code": name+str(idx),
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

def get_and_inherit_base_type(Node):
    # get base type from type keyword
    match Node.children[0]:
        case TokenType.TYPE_INT:
            Node.base_type= "int"
            Node.base_width= 16
        case TokenType.TYPE_FLOAT:
            Node.base_type= "float"
            Node.base_width= 32
        case TokenType.TYPE_STR:
            # in case of string we do not have any possible array
            Node.type= "str"
            return
        case TokenType.TYPE_BOOL:
            Node.base_type= "bool"
            Node.base_width= 16
        case __:
            raise SyntaxError("EXPECTED TYPE SPECIFIER")
    # make array possibly inherit this base_type
    Node.children[1].base_type= Node.base_type
    Node.children[1].base_width= Node.base_width

def synth_expected_type_and_width(Node):
    if Node.type=="str":
        return
    Node.type= Node.children[1].type
    Node.width= Node.children[1].width
    
def inherit_base_type(Node):
    Node.children[3].base_type= Node.base_type
    Node.children[3].base_width = Node.base_width

def synth_array(Node):
    if Node.children[1].type != "int" or Node.children[1].calculated==False:
        raise Exception("ARRAY LENGTH SPECIFIER CAN ONLY BE CONSTANT INT")
    value= Node.children[1].value
    Node.width = value * Node.width
    Node.type = {
        "array": value,
        "type" : Node.children[1].type
    }

def stop_base_type_inheritance(Node):
    Node.type= Node.base_type
    Node.width = Node.base_width

