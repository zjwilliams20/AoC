#########################
# day 19
#########################

class LeafNode():
    def __init__(self, letter):
        self.letter = letter
    def fill(self, ind2Node):
        pass
    def match(self, string, level):
        if len(string) == 0: 
            return set()
        if string[0] == self.letter:
            return set([string[1:]])
        return set()
    def __str__(self, level=0):
        return '  ' * level + f'LEAF "{self.letter}"'

class OrNode():
    def __init__(self, left, right):
        self.left  = left
        self.right = right
    def fill(self, ind2Node):
        self.left.fill(ind2Node)
        self.right.fill(ind2Node)
    def match(self, string, level):
        leftStrings = self.left.match(string, level+1)
        rightStrings = self.right.match(string, level+1)
        return leftStrings | rightStrings
    def __str__(self, level=0):
        return '  ' * level + f'OR {self.id}'

class AndNode():
    def __init__(self, children):
        self.children = children
    def fill(self,ind2Node):
        if not isinstance(self.children[0],int): return
        for idx, idxChild in enumerate(self.children):
            child=ind2Node.get(idxChild,None)
            self.children[idx]=child
            child.fill(ind2Node)

    def match(self, string, level=0):
        currList = set([string])
        for child in self.children:
            # reset next list to current
            nextList = set()

            # update the future child's list
            [nextList.update(child.match(string, level+1)) for string in currList]
            
            # quit if the current child didn't have any matches
            if len(nextList) == 0: return set()

            # update the current list for the next child
            currList = nextList
        return nextList
    def __str__(self, level=0):
        return '  ' * level + f'AND {self.id}'

# load input
with open('input/day19', 'r') as file:
    evth = [line.strip() for line in file.readlines()]

# define rules
rulebook = evth[:129]

def addRule(rule, ind2Node):
    '''define a node from a rule and add the dict, e.g. "3: 4 5 | 5 4"'''

    name, children = rule.split(':')
    # nothing more to do
    if 'a' in children:
        ind2Node[int(name)] = LeafNode('a')
        return ind2Node
    if 'b' in children:
        ind2Node[int(name)] = LeafNode('b')
        return ind2Node
    
    # define OrNode with two GroupNodes
    if '|' in children:
        left, right = children.split('|')

        leftGroup  = AndNode([int(s) for s in left.split() if s.isdigit()])
        rightGroup = AndNode([int(s) for s in right.split() if s.isdigit()])
        
        ind2Node[int(name)] = OrNode(leftGroup, rightGroup)
        return ind2Node

    # define GroupNode
    else:
        ind2Node[int(name)] = AndNode([int(s) for s in children.split() if s.isdigit()])
        return ind2Node

# construct rules
ind2Node = {}
for rule in rulebook:
    ind2Node = addRule(rule, ind2Node)

# fill the tree
tree = ind2Node[0]
tree.fill(ind2Node)

# construct messages
messages = [msg for msg in evth[130:]]

# find how many messages were valid
nValid = sum(['' in tree.match(msg) for msg in messages])
print(f'Found {nValid} valid messages')
