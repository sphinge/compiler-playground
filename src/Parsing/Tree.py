from Lexing.TokenTypes import TokenType
from Semantic.SDDHash import SDDHash
import pydot

class Tree_Wrapper():
    def __init__(self):
        self.root  = None
        self.dot   = pydot.Dot("ParseTree", graph_type="digraph")
        self.edges = []
        self.nodes = []
        self.size  = 0

    def addNode(self, name: str, parentID: int|None = None, literal: str|None = None, loc: tuple[int,int]|None = None):
        if parentID == None:
            self.size += 1
            self.root = Tree_Node(str(self.size), label = name)
            self.nodes.append(self.root)
            return self.size

        parent = self.find(str(parentID))

        if parent == None:
            raise Exception(f"NO PARENT-NODE WITH ID {parentID}")
        
        self.size += 1
        self.edges.append((str(self.size),str(parentID)+"\n"))

        newNode = Tree_Node(str(self.size), label=name)
        newNode.lexval = literal
        if loc is not None:
            newNode.loc = loc
        parent.add_child(newNode)

        self.nodes.append(newNode)
        
        return self.size

    def find(self, ID):
        if type(ID) != str:
            ID = str(ID)

        return self.root.search(ID)

    def print(self, DEBUG=False):
        for i, node in enumerate(self.nodes):
            print(f"Printing Tree ... Creating Node {i} of {self.size}")
            if node.lexval:
                label= f"{node.label}: {node.lexval}"
            else:
                label= node.label

            if DEBUG and node.code:
                label += "\n"+ str(node.code)
            self.dot.add_node(pydot.Node(str(node.ID), label = label))

        
        for i, j in (self.edges):
            print(f"Printing Tree ... Creating edges")
            self.dot.add_edge(pydot.Edge(j,i))
        print("Printing Tree to output.png")
        self.dot.write_png("output.png")                

    def add_SDD_function_handles(self, token: tuple[str, int], production: list):
        first_element_of_production = production[0] if type(production[0]) == str else TokenType.token_type_to_string(production[0])
        sdd_function_handles = SDDHash[token[0]][first_element_of_production]

        node = self.find(token[1])
        if node:
            emptySDDValue = "$$$$"
            if sdd_function_handles == emptySDDValue:
                node.SDD_inherit_func = emptySDDValue
            else:
                node.SDD_inherit_func = sdd_function_handles[0]
                node.SDD_synthesize_func = sdd_function_handles[1]

    def execute_IRGeneration(self) -> str:
        self.root.run_SDDs()
        return self.root.code


class Tree_Node():
    def __init__(self, ID, label):
        # Basic Tree Logic
        self.ID       = ID
        self.children = []
        self.label    = label

        # SDD logic
        self.SDD_inherit_func    = None
        self.SDD_synthesize_func = None
        self.lexval     = None
        self.loc        = (None,None)

        # SDD TypChecking
        self.type = None

        # SDD IR Generation
        self.code           = None
        self.res            = None
        self.managed_labels = {}
        self.next           = None
        self.true_label     = None
        self.false_label    = None
        self.operand        = None
        
    def add_child(self, new):
        self.children.append(new)

    def search(self,ID):
        if self.ID == ID:
            return self
        
        for i in self.children:
            ret = i.search(ID)
            if ret != None:
                return ret

    def run_SDDs(self):
        # if functions are not yet implemented
        if self.SDD_inherit_func == "$$$$":
            self.code = f"\n // --------------------- \n // Code for {self.label} \n // --------------------- \n"
            self.type = f"{self.label}.type"
            return
        
        cond1 = TokenType.string_to_token_type(self.label.upper()) == None
        cond2 = self.label != "epsilon"
        labelIsNonterminal = cond1 and cond2
        
        if labelIsNonterminal:
            if self.SDD_inherit_func:
                self.SDD_inherit_func(self)

            for child in (self.children):
                child.run_SDDs()

            if self.SDD_synthesize_func:
                self.SDD_synthesize_func(self)
        

class SDD_Handlers():
    @staticmethod
    def get(NonTerminal: str, Production:list):
        return SDDHash()


if __name__ == "__main__":
    a = Tree_Wrapper()
    a.addNode("test1")
    a.addNode("test2", 1)
    a.addNode("test3", 2)

    a.addNode("test4", 2)

    a.print()
