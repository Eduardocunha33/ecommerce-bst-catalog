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
        #cria a lista vazia onde os produtos dentro da faixa serao guardados
        resultList = []
        #a funcao recursiva preenche a resultList e devolve o total de nos visitados
        visitedNodes = self.searchByPriceRangeRecursive(self.root, minPrice, maxPrice, resultList)
        #devolve dois valores ao mesmo tempo (a lista filtrada e o contador)
        return resultList, visitedNodes

    def searchByPriceRangeRecursive(self, node, minPrice, maxPrice, resultList):
        #caso base - se chegou em um galho vazio (None), nao visitou nenhum no (retorna 0)
        if node is None:
            return 0

        #comeca em 1 porque a arvore acabou de entrar e analisar este no atual
        visited = 1

        #so desce para a esquerda se ainda puder existir preco >= minPrice, somando os nos visitados la
        if node.value.price > minPrice:
            visited += self.searchByPriceRangeRecursive(node.left, minPrice, maxPrice, resultList)

        #se o preco do no atual esta dentro do intervalo, adiciona o produto na lista
        if minPrice <= node.value.price <= maxPrice:
            resultList.append(node.value)

        #so desce para a direita se ainda puder existir preco <= maxPrice, somando os nos visitados la
        if node.value.price <= maxPrice:
            visited += self.searchByPriceRangeRecursive(node.right, minPrice, maxPrice, resultList)

        #devolve para quem chamou o total de nos visitados a partir deste ponto
        return visited

    def countNodes(self):
        #inicia a contagem total de produtos na arvore a partir da raiz
        return self.countNodesRecursive(self.root)

    def countNodesRecursive(self, node):
        #se o no for vazio, contribui com 0 na contagem
        if node is None:
            return 0
        #soma 1 (o no atual) + tudo que existe na esquerda + tudo que existe na direita
        return 1 + self.countNodesRecursive(node.left) + self.countNodesRecursive(node.right)