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
        Product("Xbox One (Original)", "Console", "500 GB", 1100.00, 5),
        Product("HyperX Cloud Stinger 2 Wireless", "Headset", "Wireless", 559.90, 8),
        Product("PlayStation 4 Slim", "Console", "1 TB", 1890.00, 6),
        Product("Razer Basilisk V3", "Mouse", "Com fio", 349.90, 12),
        Product('Monitor 27" Full HD', "Monitor", "144Hz IPS", 799.90, 7),
        Product("PlayStation 4 Fat (Original)", "Console", "1 TB", 1490.00, 4),
        Product("PlayStation 5 Slim (Digital)", "Console", "1 TB", 3999.00, 10),

        # --- Distribuicao intermediaria ---
        Product("Controle DualShock 4", "Controle", "PlayStation 4", 199.90, 15),
        Product("Controle Sem Fio DualSense", "Controle", "PlayStation 5", 449.90, 14),
        Product('Monitor 24" Full HD', "Monitor", "Basico", 599.90, 10),
        Product("Intel Core i5-12400F", "Processador", "6 Nucleos / 12 Threads", 979.90, 9),
        Product("PlayStation 4 Fat (Original)", "Console", "500 GB", 1299.00, 3),
        Product("Razer Naga V3 Pro", "Mouse", "Sem fio", 1699.90, 4),
        Product("PlayStation 4 Pro", "Console", "1 TB", 2200.00, 5),
        Product("PlayStation 5 Slim (Com Disco)", "Console", "1 TB", 4599.00, 8),

        # --- Restante dos itens (perifericos, monitores, processadores e consoles) ---
        Product("Razer DeathAdder Essential", "Mouse", "Com fio", 179.90, 20),
        Product("HyperX Cloud Stinger 2 Core", "Headset", "Com fio", 209.90, 18),
        Product("Razer Cobra", "Mouse", "Com fio", 279.90, 15),
        Product("Controle Sem Fio Xbox One", "Controle", "Xbox One", 289.90, 10),
        Product("Razer DeathAdder V2 X HyperSpeed", "Mouse", "Sem fio", 389.90, 11),
        Product("Controle Sem Fio Xbox Series X|S", "Controle", "Xbox Series X|S", 399.90, 13),
        Product("AMD Ryzen 3 3200G", "Processador", "4 Nucleos / Video Integrado", 399.99, 10),
        Product("HyperX Cloud III", "Headset", "Com fio", 419.90, 9),
        Product('Monitor 21,5" Full HD', "Monitor", "Basico", 479.90, 12),
        Product("AMD Ryzen 5 5500", "Processador", "6 Nucleos / 12 Threads", 549.99, 14),
        Product("Razer Viper V3 Pro", "Mouse", "Sem fio", 699.90, 6),
        Product('Monitor 24" Full HD Gamer', "Monitor", "180Hz", 849.90, 8),
        Product("HyperX Cloud III Wireless", "Headset", "Sem fio", 859.90, 7),
        Product('Monitor 31,5" / 32" Full HD', "Monitor", "144Hz", 1089.90, 5),
        Product("AMD Ryzen 5 7600X", "Processador", "6 Nucleos / AM5", 1089.99, 7),
        Product("AMD Ryzen 7 5700X", "Processador", "8 Nucleos / 16 Threads", 1199.99, 8),
        Product("Xbox One", "Console", "1 TB", 1399.00, 4),
        Product('Monitor 27" QHD / 4K', "Monitor", "Alta Resolucao", 1499.90, 6),
        Product("Intel Core i7-12700F", "Processador", "12 Nucleos / 20 Threads", 1579.99, 5),
        Product("PlayStation 4 Slim", "Console", "500 GB", 1650.00, 4),
        Product("AMD Ryzen 7 7800X3D", "Processador", "8 Nucleos / AM5", 1769.99, 4),
        Product('Monitor 32" 4K', "Monitor", "Alta Resolucao", 1999.90, 3),
        Product("Intel Core i7-14700K", "Processador", "20 Nucleos / 28 Threads", 1999.99, 4),
        Product("Xbox Series S", "Console", "512 GB", 3199.00, 9),
        Product("Xbox Series S", "Console", "1 TB", 3899.00, 7),
        Product("Xbox Series X", "Console", "1 TB", 4499.00, 6),
        Product("PlayStation 5 Pro", "Console", "2 TB", 7399.00, 3),
    ]

    # Percorre a lista e insere cada produto dentro da arvore que foi passada por parametro
    for product in initialProducts:
        catalogTree.insert(product)