class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class BinaryTree:
    def __init__(self):
        self.root = None

    def insert(self, data):
        # cria o nó que vai ser inserido na árvore
        newNode = Node(data)

        # verifica se a árvore está vazia, se estiver, o nó inserido será a raiz da árvore
        if (self.isEmpty()):
            self.root = newNode
            return

        self.insertRecursive(self.root, newNode)

    def insertRecursive(self, currentNode, newNode):
        # verifica se o nó da esquerda é None, se for, insere o novo nó na esquerda
        if newNode.value < currentNode.value:
            if currentNode.left is None:
                currentNode.left = newNode
            else:
                self.insertRecursive(currentNode.left, newNode)
        else:
            if currentNode.right is None:
                currentNode.right = newNode
            else:
                self.insertRecursive(currentNode.right, newNode)

    # retorna True se a árvore estiver vazia, caso contrário, retorna False
    def isEmpty(self):
        return self.root == None

    # 1. Pré-ordem (Raiz, Esquerda, Direita)
    def preOrder(self):
        self.preOrderRecursive(self.root)
        print()

    def preOrderRecursive(self, node):
        if node is not None:
            print(node.value, end=" ")
            self.preOrderRecursive(node.left)
            self.preOrderRecursive(node.right)

    # 2. Em-ordem (Esquerda, Raiz, Direita)
    def inOrder(self):
        self.inOrderRecursive(self.root)
        print()

    def inOrderRecursive(self, node):
        if node is not None:
            self.inOrderRecursive(node.left)
            print(node.value, end=" ")
            self.inOrderRecursive(node.right)

    # 3. Pós-ordem (Esquerda, Direita, Raiz)
    def postOrder(self):
        self.postOrderRecursive(self.root)
        print()

    def postOrderRecursive(self, node):
        if node is not None:
            self.postOrderRecursive(node.left)
            self.postOrderRecursive(node.right)
            print(node.value, end=" ")

    # --- Novos métodos para o catálogo de e-commerce ---

    def getAllInOrder(self):
        productsList = []
        self.getAllInOrderRecursive(self.root, productsList)
        return productsList

    def getAllInOrderRecursive(self, node, productsList):
        if node is not None:
            self.getAllInOrderRecursive(node.left, productsList)
            productsList.append(node.value)
            self.getAllInOrderRecursive(node.right, productsList)

    def findMin(self):
        if self.isEmpty():
            return None
        currentNode = self.root
        while currentNode.left is not None:
            currentNode = currentNode.left
        return currentNode.value

    def findMax(self):
        if self.isEmpty():
            return None
        currentNode = self.root
        while currentNode.right is not None:
            currentNode = currentNode.right
        return currentNode.value

    def searchByPriceRange(self, minPrice, maxPrice):
        resultList = []
        self.searchByPriceRangeRecursive(self.root, minPrice, maxPrice, resultList)
        return resultList
        #Esse método retorna uma lista de produtos que estão dentro da faixa de preço especificada (minPrice, maxPrice).

    def searchByPriceRangeRecursive(self, node, minPrice, maxPrice, resultList):
        if node is None:
            return
        #Este método é chamado recursivamente para percorrer a árvore binária de busca e encontrar os produtos que estão dentro da faixa de preço especificada. Ele utiliza a propriedade da árvore binária de busca para otimizar a busca, evitando explorar ramos que não podem conter produtos dentro da faixa de preço.

        # 1. Só explora a esquerda se ainda puder existir algo >= minPrice
        if node.value.price > minPrice:
            self.searchByPriceRangeRecursive(node.left, minPrice, maxPrice, resultList)

        # 2. Se o produto atual está dentro da faixa, guarda na lista
        if minPrice <= node.value.price <= maxPrice:
            resultList.append(node.value)

        # 3. Só explora a direita se ainda puder existir algo <= maxPrice
        if node.value.price <= maxPrice:
            self.searchByPriceRangeRecursive(node.right, minPrice, maxPrice, resultList)