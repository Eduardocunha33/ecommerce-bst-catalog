# Importamos a classe Product para conseguir criar os objetos dos produtos
from product import Product


def loadCatalog(catalogTree):
    # Lista com os 42 produtos iniciais do e-commerce.
    # IMPORTANTE: Os itens estao em ordem misturada de preco propositalmente,
    # comecando por um valor intermediario (R$ 1.100,00).
    # Motivo: se inserirmos tudo ja ordenado do mais barato ao mais caro,
    # a BST vira uma "linha reta" para a direita e perde a velocidade de busca.
    initialProducts = [
        # --- Primeiros nos para equilibrar os galhos da arvore ---
        Product("Xbox One", "Console", "500 GB", 1100.00, 5, "images/Xbox One (Original).jpg"),
        Product("HyperX Cloud Stinger 2 Wireless", "Headset", "Wireless", 559.90, 8, "images/HyperX Cloud Stinger 2 Wireless.jpg"),
        Product("PlayStation 4 Slim", "Console", "1 TB", 1890.00, 6, "images/PlayStation 4 Slim.jpg"),
        Product("Razer Basilisk V3", "Mouse", "Com fio", 349.90, 12, "images/Razer Basilisk V3.jpg"),
        Product('Monitor 27" Full HD', "Monitor", "144Hz IPS", 799.90, 7, "images/Monitor 27 Pol Full HD.jpg"),
        Product("PlayStation 4 Fat", "Console", "1 TB", 1490.00, 4, "images/PlayStation 4 Fat.jpg"),
        Product("PlayStation 5 Slim", "Console", "1 TB", 3999.00, 10, "images/PlayStation 5 Slim.jpg"),

        # --- Distribuicao intermediaria ---
        Product("Controle DualShock 4", "Controle", "PlayStation 4", 199.90, 15, "images/Controle DualShock 4.jpg"),
        Product("Controle Sem Fio DualSense", "Controle", "PlayStation 5", 449.90, 14, "images/Controle Sem Fio DualSense.jpg"),
        Product('Monitor 24" Full HD', "Monitor", "Basico", 599.90, 10, "images/Monitor 24 Full HD.jpg"),
        Product("Intel Core i5-12400F", "Processador", "6 Nucleos / 12 Threads", 979.90, 9, "images/Intel Core i5-12400F.jpg"),
        Product("PlayStation 4 Fat", "Console", "500 GB", 1299.00, 3, "images/PlayStation 4 Fat.jpg"),
        Product("Razer Naga V3 Pro", "Mouse", "Sem fio", 1699.90, 4, "images/Razer Naga V3 Pro.jpg"),
        Product("PlayStation 4 Pro", "Console", "1 TB", 2200.00, 5, "images/PlayStation 4 Pro.jpg"),
        Product("PlayStation 5 Slim (Com Disco)", "Console", "1 TB", 4599.00, 8, "images/PlayStation 5 Slim.jpg"),

        # --- Restante dos itens (perifericos, monitores, processadores e consoles) ---
        Product("Razer DeathAdder Essential", "Mouse", "Com fio", 179.90, 20, "images/Razer DeathAdder Essential.jpg"),
        Product("HyperX Cloud Stinger 2 Core", "Headset", "Com fio", 209.90, 18, "images/HyperX Cloud Stinger 2 Core.jpg"),
        Product("Razer Cobra", "Mouse", "Com fio", 279.90, 15, "images/Razer Cobra.jpg"),
        Product("Controle Sem Fio Xbox One", "Controle", "Xbox One", 289.90, 10, "images/Controle Sem Fio Xbox One.jpg"),
        Product("Razer DeathAdder V2 X HyperSpeed", "Mouse", "Sem fio", 389.90, 11, "images/Razer DeathAdder V2 X HyperSpeed.jpg"),
        Product("Controle Sem Fio Xbox Series X|S", "Controle", "Xbox Series X|S", 399.90, 13, "images/Controle Sem Fio Xbox Series XS.jpg"),
        Product("AMD Ryzen 3 3200G", "Processador", "4 Nucleos / Video Integrado", 399.99, 10, "images/AMD Ryzen 3 3200G.jpg"),
        Product("HyperX Cloud III", "Headset", "Com fio", 419.90, 9, "images/HyperX Cloud III.jpg"),
        Product('Monitor 21,5" Full HD', "Monitor", "Basico", 479.90, 12, "images/Monitor 21,5 Full HD.jpg"),
        Product("AMD Ryzen 5 5500", "Processador", "6 Nucleos / 12 Threads", 549.99, 14, "images/AMD Ryzen 5 5500.jpg"),
        Product("Razer Viper V3 Pro", "Mouse", "Sem fio", 699.90, 6, "images/Razer Viper V3 Pro.jpg"),
        Product('Monitor 24" Full HD Gamer', "Monitor", "180Hz", 849.90, 8, "images/Monitor 24 Full HD Gamer.jpg"),
        Product("HyperX Cloud III Wireless", "Headset", "Sem fio", 859.90, 7, "images/HyperX Cloud III Wireless.jpg"),
        Product('Monitor 31,5" / 32" Full HD', "Monitor", "144Hz", 1089.90, 5, "images/Monitor 31,5.jpg"),
        Product("AMD Ryzen 5 7600X", "Processador", "6 Nucleos / AM5", 1089.99, 7, "images/AMD Ryzen 5 7600X.jpg"),
        Product("AMD Ryzen 7 5700X", "Processador", "8 Nucleos / 16 Threads", 1199.99, 8, "images/AMD Ryzen 7 5700X.jpg"),
        Product("Xbox One", "Console", "1 TB", 1399.00, 4, "images/Xbox One (Original).jpg"),
        Product('Monitor 27" QHD / 4K', "Monitor", "Alta Resolucao", 1499.90, 6, "images/Monitor 27 Pol Full HD.jpg"),
        Product("Intel Core i7-12700F", "Processador", "12 Nucleos / 20 Threads", 1579.99, 5, "images/Intel Core i7-12700F.jpg"),
        Product("PlayStation 4 Slim", "Console", "500 GB", 1650.00, 4, "images/PlayStation 4 Slim.jpg"),
        Product("AMD Ryzen 7 7800X3D", "Processador", "8 Nucleos / AM5", 1769.99, 4, "images/AMD Ryzen 7 7800X3D.jpg"),
        Product('Monitor 32" 4K', "Monitor", "Alta Resolucao", 1999.90, 3, "images/Monitor 32 4K.jpg"),
        Product("Intel Core i7-14700K", "Processador", "20 Nucleos / 28 Threads", 1999.99, 4, "images/Intel Core i7-14700K.jpg"),
        Product("Xbox Series S", "Console", "512 GB", 3199.00, 9, "images/Xbox Series S.jpg"),
        Product("Xbox Series S", "Console", "1 TB", 3899.00, 7, "images/Xbox Series S.jpg"),
        Product("Xbox Series X", "Console", "1 TB", 4499.00, 6, "images/Xbox Series X.jpg"),
        Product("PlayStation 5 Pro", "Console", "2 TB", 7399.00, 3, "images/PlayStation 5 Pro.jpg"),
    ]

    # Percorre a lista e insere cada produto dentro da arvore que foi passada por parametro
    for product in initialProducts:
        catalogTree.insert(product)