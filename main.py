from product import Product
from tree import BinaryTree

catalog = BinaryTree()

sampleProducts = [
    Product("PlayStation 4 Slim", "Console", "1 TB", 1890.00),
    Product("Razer Cobra", "Mouse", "Com fio", 279.90),
    Product("PlayStation 5 Slim (Digital)", "Console", "1 TB", 4490.00),
    Product("HyperX Cloud III", "Headset", "Com fio", 419.90),
    Product('Monitor 27" Full HD', "Monitor", '27" (144Hz IPS)', 799.90),
]

for item in sampleProducts:
    catalog.insert(item)

print("Catálogo ordenado por preço (inOrder):")
catalog.inOrder()