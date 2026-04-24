class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

class Solution:
    def mergeTrees(self, t1: Node, t2: Node) -> Node:
        if not t1 and not t2:
            return None
        elif not t1:
            return t2
        elif not t2:
            return t1

        # Both nodes exist, so we create a new node with the sum of their values
        newNode = Node(t1.value + t2.value)
        newNode.left = self.mergeTrees(t1.left, t2.left)
        newNode.right = self.mergeTrees(t1.right, t2.right)

        return newNode
