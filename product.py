class Product:
    def __init__(self, name, category, specs, price, stock=10, image=""):
        self.name = name
        self.category = category
        self.specs = specs
        self.price = price
        self.stock = stock
        self.image = image

    def __lt__(self, other):
        return self.price < other.price

    def __str__(self):
        return f"{self.name} ({self.specs}) - R$ {self.price:.2f}"