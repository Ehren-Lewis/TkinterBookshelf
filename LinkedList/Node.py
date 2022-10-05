class Node:
    """
    Nodes are a basic data structure which contain data and one or more links to other nodes.
    Nodes can be used to represent a tree structure or a linked list.
    In such structures where nodes are used, it is possible to traverse from one node to another node.
    """

    def __init__(self, value):
        self.value = value
        self.next_node = None

    def get_value(self):
        return self.value

    def set_next_node(self, node):
        """
        Data structures containing nodes have typically two bits of information stored in a node:
        data and link to next node.The first part is a value and the second part is an address of sorts pointing to
         the next node. In this way, a system of nodes is created.A NULL value in the link part of a node’s info
         denotes that the path or data structure contains no further nodes.
        """
        self.next_node = node

    def get_next_node(self):
        return self.next_node