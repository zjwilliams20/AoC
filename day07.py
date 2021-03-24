#########################
# day 7
#########################

import csv
import re

def findPattern(pattern, string):
    match = re.findall(pattern, string)
    return match if match else None

class Tree():
    def __init__(self, root):
        self.root = defineNode(root)
    def __str__(self):
        return self.root.__str__()


class Node():
    def __init__(self, name, children=None, amount=0, defined=True):
        if children is None:
            children = []
        self.name = name
        self.children = children
        self.amount = amount
        self.defined = defined
    def addChild(self, child):
        self.children.append(child)
    def __hash__(self):
        return hash(self.name)
    def __repr__(self):
        return self.__str__()
    def __str__(self, level=0):
        childStr=''
        if self.children:
            for child in self.children:
                childStr += child.__str__(level+1)
        if self.defined:
            defChar = '\u2713'
        else:
            defChar = 'X'
        if level == 0:
            return f"{defChar} {self.name}\n" + childStr
        else:
            return "  " * level + f"{defChar} - {self.amount} {self.name}\n" + childStr


def buildNode(string):
    '''Create a node from a string'''

    name = findPattern("^\w+ \w+", string)
    parent = Node(*name)

    childList = findPattern("\d+ \w+ \w+", string)
    if childList is not None:
        for c in childList:
            amount, childName = str.split(c, ' ', 1)
            parent.addChild(Node(childName, [], int(amount), False))
        return parent
    return Node(*name, defined=True)

def defineNode(node):
    '''Define all children within a node, i.e. grow upward toward the leaves'''

    if not node.defined:
        node.children = findRule(node.name, rulebook)
        node.defined = True
    if node.children:
        for child in node.children:
            child = defineNode(child)
    return node

def hasNode(node, name, level=0):
    '''Determine if the node contains another particular node'''
    if node.name == name and level != 0:
        return True
    if node.children:
        ans = []
        for child in node.children:
            ans.append(hasNode(child, name, level+1))
        return any(ans)
    return False

def countNode(node, multiplier=1):
    '''Count how many nodes are inside a node, excluding the parent'''

    # initialize to the amount at the current level
    childrSum = multiplier * node.amount

    # fix for top level
    if node.amount == 0:
        node.amount = 1

    if node.children:
        for child in node.children:
            childrSum += countNode(child, multiplier*node.amount)
        return childrSum
    else:
        return multiplier * node.amount

def findRule(name, rulebook):
    '''Find a rule in the rulebook, return its children'''
    for rule in rulebook:
        if name == rule.name:
            return rule.children
    raise AssertionError(f'<ERROR: unable to find rule "{name}" in rulebook!>')

# load data
rulebook = []
with open("input/day7", 'r') as file:
    reader = csv.reader(file, delimiter='\n')
    rulebook = [buildNode(*line) for line in reader if line]

# grow the forest
forest = []
for rule in rulebook:
    forest.append(Tree(rule))
print(*forest)

# part 1
hasShinyGold = 0
for tree in forest:
    hasShinyGold += hasNode(tree.root, 'shiny gold')
print(f"FOUND {hasShinyGold} BAGS W/ SHINY GOLD!!!\n")

# part 2
for tree in forest:
    if tree.root.name == "shiny gold":
        print(f"{tree.root.name} HAVE {countNode(tree.root)} OTHER BAGS!")
        break
