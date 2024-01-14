"""
FILE SDD FUNCTIONS

WRITE NECESSARY FUNCTIONS FOR EACH PRODCUTION HERE

Include the function name in the appropriate place of the SDDHash

I think the functions should only take one node as input. This node is defined in Tree.py
"""
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