"""
FILE SDD FUNCTIONS

WRITE NECESSARY FUNCTIONS FOR EACH PRODCUTION HERE

Include the function name in the appropriate place of the SDDHash

I think the functions should only take one node as input. This node is defined in Tree.py
"""

from Lexing.TokenTypes import TokenType
from SymboltableStack import SymboltableStack

#--------------------
# SYMBOL TABLE
symbolTable= SymboltableStack()
# SYMBOL TABLE
#--------------------

#-------------------------
# LABEL

class Label():
    # LABELS
    number_of_labels = 0
    all_labels = []
    def __init__(self, name:str= "") -> None:
        idx = Label.number_of_labels
        Label.number_of_labels+=1
        Label.all_labels.append(self)
        self.code =  name + str(idx) + ":\n"
        self.name =  name+ str(idx)
        self.id   =  idx
        self.WasUsed = False
        
    def get(self):
        self.WasUsed = True
        return self.name

    def set(self, force = False):
        if self.WasUsed or force:
            return [self.code]
        else:
            return []
        

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
        "name": "t"+str(idx),
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
    node.code = node.children[0].code + node.managed_labels["next"].set() + node.children[1].code

def inherit_next_1_child(node):
    node.children[0].next = node.next

def synth_code_1_child(node):
    node.code = node.children[0].code

def synth_code_epsilon(node):
    node.code = []

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
        case TokenType.TYPE_STR:
            node.type= "string"
            node.width= None
        case TokenType.TYPE_BOOL:
            node.type= "bool"
            node.width= 16
        case __:
            raise SyntaxError("EXPECTED TYPE SPECIFIER")
        
    node.code= [node.type]
    
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
    symbolTable.addSymbolToCurrentContext(node.children[1].lexval, None, expected_type)    #node.symbol_table.add?

    if node.children[0].code == ["string"]:
        node.children[0].code = ["char"]
        node.children[1].lexval+="[]"
    # SYNTH CODE
    node.code = node.children[3].code + node.children[0].code + [f'{node.children[1].lexval} = {node.children[3].res["name"]};']

def EXPRSTMT_synth(node):
    node.type = node.children[0].type
    node.res = node.children[0].res
    node.code = node.children[0].code

def IFSTMT_inherit(node):
    T = Label("Cond_True")
    F = Label("Cond_False")

    node.children[2].true_label  = T
    node.children[2].false_label = F
    node.managed_labels["True"]  = T
    node.managed_labels["False"] = F
    
    true_next = node.next
    node.children[5].next = true_next

    node.children[7].next = node.next

def IFSTMT_synth(node):
    expression = node.children[2]
    statement1 = node.children[5]
    ifstmtx = node.children[7]
    node.code = expression.code + node.managed_labels['True'].set() + statement1.code + node.managed_labels['False'].set() + ifstmtx.code
    
def IFSTMTX_synth(node):
    statement = node.children[2]
    node.code =  statement.code
    
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
    node.code= node.managed_labels['start'].set(force = True) + expression.code + node.managed_labels['True'].set() + statement.code + ["goto"] + [node.managed_labels['start'].get()+";"]
    
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
        case _:
            c_type_id= f'C-typeSpecifier({expression.type})'
    
    node.code= expression.code + node.managed_labels["EXPR_next"].set() + [f'printf("{c_type_id}", {expression.res["name"]});']
    
def RETSTMT_inherit(node):
    expression= node.children[1]
    next=  Label("next")
    expression.next= next
    node.managed_labels["EXPR_next"]=next
    
def RETSTMT_synth(node):
    expression= node.children[1]

    if expression.type!="int":
        raise Exception("TYPE ERROR: only return int")

    node.code= expression.code + node.managed_labels["EXPR_next"].set() + [f'return {expression.res["name"]};']
    
def EXPR_inherit(node):
    for child in node.children:
        if node.true_label:
            child.true_label= node.true_label
        if node.false_label:
            child.false_label= node.false_label
    
def EXPR_bool_highest_add_gotos(node):
    EXPR_bool_synth(node)
    if node.true_label and node.false_label:
        node.code+= [ f'if ({node.res["name"]}) {"{"} goto {node.true_label.get()};{"}"}', f'if (!({node.res["name"]})) {"{"} goto {node.false_label.get()};{"}"}' ]

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
    
    if exprx.code==[] and exprx.res==None:
        node.res= elevel1.res
        node.code=elevel1.code
    else:
        node.res= Temp("bool")
        exprx_code= exprx.code if exprx.code!=None else ""
        node.code = elevel1.code + exprx_code + [f'{node.res["code"]} = {elevel1.res["name"]} {operand} {exprx.res["name"]}; ']
  
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
        node.code = elevel1.code + exprx.code + [f'{node.res["code"]} = {elevel1.res["name"]} {operand} {exprx.res["name"]}; ']
    else:
        node.res= elevel1.res
        node.code= elevel1.code

def EXPRX3_synth(node):
    node.operand= node.children[0].code 
    expr = node.children[1]
    
    node.res = expr.res
    node.code = expr.code

def EXPRX_synth(node):
    node.operand= node.children[0].label
    expr = node.children[1]
    
    node.res = expr.res
    node.code = expr.code
    
def EXPR_invert_synth(node):
    operant_token= node.children[0].label
    expr = node.children[1]
    
    node.type = expr.type
    if node.type=="str":
        print("TYPE ERROR")
    
    node.res = Temp(node.type)
    node.code =[f'{expr.code} \n {node.res} = {operant_token} {expr.res}']
    
def EXPR_L6_synth(node):
    node.code= node.children[0].code
    node.res = node.children[0].res
    node.type = node.children[0].type

def EXPR_PRIMARY_synth(node):
    only_child= node.children[0]
    node.type = only_child.type
    node.res = only_child.res
    node.code = [only_child.code]

def EXPR_PRIMARY_getValue_synth(node):
    child= node.children[0]

    node.code= []
    match child.label:
        case "true":
            node.type="bool"
            node.res={"name":"true"}
        case "false":
            node.type="bool"
            node.res={"name":"false"}
        case "string":      # add extra "" to string 
            node.type="string"
            node.res={"name": f'"{child.lexval}"'}
        case _:
            node.type= child.label
            node.res= {"name":child.lexval}
            
def EXPR_identifier_synth(node):
    funcOrVar = node.children[0]
    node.code= funcOrVar.code
    node.res= funcOrVar.res
    node.type = funcOrVar.type
    
def VARORCALL_synth(node):
    identifier = node.children[0]
    variablename= identifier.lexval
    tableEntry= symbolTable.get(variablename)
    if not tableEntry:
        print("UNDEFINED ERROR")
    else: 
        node.type= tableEntry["type"]
    
    funcallx= node.children[1]
    if not funcallx.res:
        node.res = {"name":variablename}
        node.code = []
    else: # THIS MEANS ITS A FUNCTION
        node.res= Temp(node.type)
        node.code= funcallx.code + [f'{node.res["code"]} = {variablename}{funcallx.res}; \n']
        
def FUNCX_synth(node):
    arguments= node.children[1]
    node.code= arguments.code
    node.res= [f"({arguments.res})"]
    
def COMPOP_synth(node):
    node.code= node.children[0].label

def ARGS_synth(node):
    expression= node.children[0]
    argsX= node.children[1]
    node.code= expression.code + argsX.code
    node.res= f"{expression.res['name']}{argsX.code}"

def ARGSX_synth(node):
    expression= node.children[0]
    argsX= node.children[1]
    node.code= expression.code + argsX.code
    node.res= f",{expression.res['name']} {argsX.code}"