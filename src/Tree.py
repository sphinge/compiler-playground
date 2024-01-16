from TokenTypes import TokenType
from Semantic.SDDHash import SDDHash
import pydot
class Tree_Wrapper():
    def __init__(self):
        self.root=None
        self.dot= pydot.Dot("ParseTree", graph_type="digraph")
        self.edges=[]
        self.size=0

    def addNode(self, name:str,parentID:int|None=None):
        if parentID==None:
            self.size+=1
            self.root=MyNode(str(self.size), label=name)
            self.dot.add_node(pydot.Node(str(self.size), label=name, rank="max"))
            return self.size
        
        parent=self.find(str(parentID))
        if parent==None:
            raise Exception(f"NO NODE WITH ID {parentID}")
        
        self.size+=1
        self.edges.append((str(self.size),str(parentID)+"\n"))
        self.dot.add_node(pydot.Node(str(self.size), label=name))
        parent.add_child(MyNode(str(self.size), label=name))
        return self.size

    def addToLatestNode(self, name):
        if self.root==None:
            self.addNode(name)
        else:
            self.addNode(name, self.size)

    def find(self, ID):
        return self.root.search(ID)

    def print(self):
        for i, j in reversed(self.edges):
            self.dot.add_edge(pydot.Edge(j,i))
        self.dot.write_png("output.png")                
        
    def generate_AST(self):
        self.root.remove_NTs()

    def add_SDD_handler(self, token: tuple[str, int], production: list):
        first_element_of_production= production[0] if type(production[0])==str else TokenType.token_type_to_string(production[0])
        function = SDDHash[token[0]][first_element_of_production]
        node= self.find(tuple[1])
        if node:
            node.SDD= function



class MyNode():
    def __init__(self, ID, label):
        self.ID=ID
        self.children=[]
        self.label=label
        self.SDD=None

    def add_child(self, new):
        self.children= [new]+self.children

    def search(self,ID):
        if self.ID==ID:
            return self
        for i in self.children:
            ret= i.search(ID)
            if ret!=None:
                return ret
        
    def getInorder(self):
        return
    
    def remove_NTs(self):
        if self.label.upper() in TokenType.__members__:
            pass#print(self.label)
        for i in self.children:
            i.remove_NTs()



class SDD_Handlers():
    @staticmethod
    def get(NonTerminal: str, Production:list):
        return SDDHash()


if __name__=="__main__":
    a= Tree_Wrapper()
    a.addNode("test1")
    a.addNode("test2", 1)
    a.addNode("test3", 2)

    a.addNode("test4", 2)
    a.addToLatestNode("LOL")

    a.print()