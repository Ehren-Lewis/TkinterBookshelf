from .Node import Node

class LinkedList:
    """
    Worst time complexity for a linked list:
    Search: O(n) for retrieving anywhere from the list
    Insertion: O(1) adding to the front, O(n) adding anywhere on the list, O(n) adding to the end
    Deletion: O(1) deleting from the front, O(n) deleting anywhere on the list, O(n) deleting from the end
    """

    def __init__(self, value=None):
        self.class_list = []
        self.head_node = None
        if value is not None:
            self.head_node = Node(value)
    #
    # def __iter__(self):
    #     return self
    #
    # def __next__(self):
    #     pass

    def get_head_node(self):
        return self.head_node

    def set_new_head(self, value):
        new_head = Node(value)
        current_head = self.head_node
        if current_head.get_value() is None:
            self.head_node = new_head
            return
        self.head_node = new_head
        self.head_node.set_next_node(current_head)

    def set_last_node(self, value):
        last_node = Node(value)
        current_node = self.head_node
        if current_node is None:
            self.head_node = last_node
            return
        while current_node.get_next_node() is not None:
            current_node = current_node.get_next_node()
        current_node.set_next_node(last_node)

    def remove_by_value(self, value):
        current_node = self.head_node
        prev_node = None
        while current_node:
            if current_node.get_value() == value:
                if prev_node:
                    prev_node.set_next_node(current_node.get_next_node())
                else:
                    self.head_node = current_node.get_next_node()
                return
            prev_node = current_node
            current_node = current_node.get_next_node()

    def print_list(self):
        return_list = []
        current_node = self.head_node
        while current_node:
            return_list.append(current_node.get_value())
            current_node = current_node.get_next_node()
        return return_list

    def node_list(self):
        return_list = []
        current_node = self.head_node
        while current_node:
            return_list.append(current_node)
            current_node = current_node.get_next_node()
        return return_list

