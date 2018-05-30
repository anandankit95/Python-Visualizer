from pptree import Node, print_tree

# Construct a string representation of a node in the call tree
def build_string(func_name, args, ret):
    if(func_name == "<module>"):
        return "None"
    s = func_name + '('
    first = True
    for formal, actual in args.items():
        if first:
            first = False
            s += "{}={}".format(formal, actual)
        else:
            s += ", {}={}".format(formal, actual)

    s += "):{}".format(ret)
    return s

# Recursively build a pptree representation of the given call tree 
def build_tree(node, parent):
    # sanitize and prep the data using sensible defaults if necessary
    if 'function_name' in node:
        func_name = node['function_name']
    else:
        func_name = "<module>"

    if 'arguments' in node:
        args = node['arguments']
    else:
        args = {}

    if 'return' in node:
        ret = node['return']
    else:
        ret = "None"

    # create a pptree Node for the current node in the call tree
    root = Node(build_string(func_name, args, ret), parent)
    # recursively add Nodes for the children of the 
    # current node in the call tree
    for next in node['seq']:
        build_tree(next, root)

# given a dictionary representing a call tree, convert and print it
def visualize(d):

    root = Node("root")
    build_tree(d, root)
    print_tree(root)
