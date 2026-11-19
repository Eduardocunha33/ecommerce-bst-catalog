class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class BinaryTree:
    def __init__(self):
        self.root = None

    def insert(self, data):
        #cria o nó que vai ser inserido na árvore
        newNode = Node(data)

        #verifica se a árvore está vazia, se estiver, o nó inserido será a raiz da árvore
        if (self.isEmpty()):
            self.root = newNode
            return

        self.insertRecursive(self.root, newNode)