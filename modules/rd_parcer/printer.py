from treelib import Tree, Node

from modules.ply_lex import LexToken

def print_esp(parrafo):
    tree = Tree()

    pNode = Node("Parrafo")
    tree.add_node(pNode)

    for oracion in parrafo:
        _build_tree(oracion, tree, pNode)
    
    tree.show()

def _build_tree(astNode, tree:Tree, parent:Node) -> Node:
    match astNode:
        case None: return
        case LexToken():
            n = Node(_lexTokenStr(astNode))
            tree.add_node(n, parent)
            return n
        
        case list():
            for el in astNode: _build_tree(el, tree, parent)
            return


    children = vars(astNode)

    n = Node(type(astNode).__name__)
    tree.add_node(n, parent)

    for child in children.values():
        _build_tree(child, tree, n)


def _lexTokenStr(t:LexToken) -> str:
    return f'{t.type}({t.value})'


