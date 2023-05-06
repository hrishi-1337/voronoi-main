import graphviz

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class BinaryTree:
    def __init__(self):
        self.root = None

    def insert(self, value):
        if not self.root:
            self.root = Node(value)
        else:
            self._insert(value, self.root)

    def _insert(self, value, current_node):
        if value < current_node.value:
            if not current_node.left:
                current_node.left = Node(value)
            else:
                self._insert(value, current_node.left)
        elif value > current_node.value:
            if not current_node.right:
                current_node.right = Node(value)
            else:
                self._insert(value, current_node.right)

    def is_balanced(self):
        return self._is_balanced(self.root) != -1

    def _is_balanced(self, current_node):
        if not current_node:
            return 0

        left_height = self._is_balanced(current_node.left)
        if left_height == -1:
            return -1

        right_height = self._is_balanced(current_node.right)
        if right_height == -1:
            return -1

        if abs(left_height - right_height) > 1:
            return -1

        return max(left_height, right_height) + 1
    
    def search(self, value):
        return self._search(value, self.root)

    def _search(self, value, current_node):
        if not current_node:
            return False

        if value == current_node.value:
            return True
        elif value < current_node.value:
            return self._search(value, current_node.left)
        else:
            return self._search(value, current_node.right)
    
    def delete(self, value):
        self.root = self._delete(value, self.root)

    def _delete(self, value, current_node):
        if not current_node:
            return current_node

        if value < current_node.value:
            current_node.left = self._delete(value, current_node.left)
        elif value > current_node.value:
            current_node.right = self._delete(value, current_node.right)
        else:
            if not current_node.left:
                return current_node.right
            elif not current_node.right:
                return current_node.left

            min_right_node = self._get_min_node(current_node.right)
            current_node.value = min_right_node.value
            current_node.right = self._delete(min_right_node.value, current_node.right)

        return current_node

    def _get_min_node(self, current_node):
        while current_node.left:
            current_node = current_node.left
        return current_node

    def draw(self):
        dot = graphviz.Digraph()

        if not self.root:
            return dot
        
        def add_nodes(node):
            if node.left:
                dot.edge(str(node.value), str(node.left.value))
                add_nodes(node.left)
            if node.right:
                dot.edge(str(node.value), str(node.right.value))
                add_nodes(node.right)

        add_nodes(self.root)
        dot.node(str(self.root.value))
        return dot

tree = BinaryTree()

tree.insert(5)
tree.insert(2)
tree.insert(7)
tree.insert(1)
tree.insert(3)

dot = tree.draw()
dot.render('tree', view=True)

print("Search for 3:", tree.search(3))  
print("Search for 6:", tree.search(6)) 

tree.delete(2)

print("Updated Binary Tree:")
print(tree.root.value)
dot = tree.draw()
dot.render('tree', view=True)

print("Search for 2:", tree.search(2))

