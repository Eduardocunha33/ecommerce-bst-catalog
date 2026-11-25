# Importamos a arvore, o modelo de produto e a funcao que carrega os 42 itens
from tree import BinaryTree
from product import Product
from catalogData import loadCatalog


# Funcao auxiliar para exibir qualquer lista de produtos de forma organizada (um por linha)
def printProducts(productsList):
    # Verifica se a lista veio vazia (ex: nenhum produto encontrado no filtro)
    if not productsList:
        print("\nNo products found.")
        return

    print(f"\nTotal found: {len(productsList)} product(s)\n")
    # enumerate(..., start=1) gera uma numeracao automatica comecando em 1
    for index, product in enumerate(productsList, start=1):
        print(f"{index:02d}. [{product.category}] {product}")
        #:02d formata o numero com 2 digitos, preenchendo com zero a esquerda se necessario (ex: 01, 02, 03, ...)


def main():
    # 1. Cria a arvore vazia
    catalog = BinaryTree()

    # 2. Carrega os 42 produtos do catalogData.py dentro da arvore
    loadCatalog(catalog)

    # 3. Loop principal do menu (continua rodando ate o usuario escolher 0 para sair)
    while True:
        print("\n=== E-COMMERCE DE ELETRONICOS (BST) ===")
        print("1 - List the entire catalog (sorted by price) ")
        print("2 - Filter products by price range")
        print("3 - View the cheapest and most expensive products")
        print("4 - Register new product")
        print("0 - Exit")

        option = input("\nChoose an option: ")

        if option == "1":
            # Usa o metodo novo que devolve a lista ordenada (em vez de imprimir tudo junto)
            allProducts = catalog.getAllInOrder()
            printProducts(allProducts)

        elif option == "2":
            #try/except evita que o programa quebre se o usuario digitar letras em vez de numeros
            try:
                minPrice = float(input("Minimum price (R$): "))
                maxPrice = float(input("Maximum price (R$): "))
                # try: se o usuario digitar algo que nao seja numero, o programa nao quebra e mostra uma mensagem de erro
            except ValueError:
                print("\nInvalid value! Please enter only numbers (e.g., 500 or 1200.50).")
                continue
                #except: se o usuario digitar algo que nao seja numero, o programa nao quebra e mostra uma mensagem de erro e em seguida vem o continue que faz o programa voltar para o inicio do loop e mostrar o menu novamente sem que o programa quebre

            #Se o usuario inverter os valores sem querer, avisamos antes de buscar
            if minPrice > maxPrice:
                print("\nThe minimum price cannot be greater than the maximum price.")
                continue

            #desempacota os dois valores devolvidos pela arvore (lista filtrada e total de nos visitados)
            filteredProducts, visitedNodes = catalog.searchByPriceRange(minPrice, maxPrice)
            printProducts(filteredProducts)

            #conta o total de produtos cadastrados na arvore para comparar com uma lista comum
            totalNodes = catalog.countNodes()
            #calcula quantos produtos a arvore conseguiu pular sem precisar analisar
            skippedNodes = totalNodes - visitedNodes
            #calcula a porcentagem de economia (e evita divisao por zero se a arvore estiver vazia)
            savedPercent = (skippedNodes / totalNodes) * 100 if totalNodes > 0 else 0

            print("\n--- Search Efficiency (BST vs Standard List) ---")
            print(f"Standard list (linear search): would check all {totalNodes} products")
            print(f"Your BST (binary tree):        visited only {visitedNodes} products")
            print(f"Skipped branches:              {skippedNodes} products skipped ({savedPercent:.2f}% saved)")

        elif option == "3":
            # Busca os extremos descendo so para a esquerda (min) ou so para a direita (max)
            cheapest = catalog.findMin()
            mostExpensive = catalog.findMax()
            print(f"\nCheapest: [{cheapest.category}] {cheapest}")
            print(f"Most expensive:   [{mostExpensive.category}] {mostExpensive}")

        elif option == "4":
            # Permite adicionar um produto novo ao vivo durante a apresentacao
            name = input("Product name: ")
            category = input("Category (Console, Monitor, Mouse, etc.): ")
            specs = input("Specification (e.g., 1 TB, Wireless, 27 inches): ")
            try:
                price = float(input("Price (R$): "))
            except ValueError:
                print("\nInvalid price! Registration canceled.")
                continue

            # Cria o objeto Product e insere na arvore mantendo a ordenacao automatica
            newProduct = Product(name, category, specs, price)
            catalog.insert(newProduct)
            print(f"\nProduct registered successfully: {newProduct}")

        elif option == "0":
            print("\nClosing the system...")
            break

        else:
            print("\nInvalid option. Please try again.")


# Garante que a funcao main() so rode quando este arquivo for executado diretamente
if __name__ == "__main__":
    main()