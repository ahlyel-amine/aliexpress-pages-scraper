
class Product:

    def __init__(self, productTitle, productRevRate, productSolde, productShipping, productPrice, productOldPrice):
        self.productTitle = productTitle
        self.productRevRate = productRevRate
        self.productSolde = productSolde
        self.productShipping = productShipping
        self.productPrice = productPrice
        self.productOldPrice = productOldPrice


    def clean(self):
        for i in range(len(self.productSolde)):
            if not self.productSolde[i].isdigit() and self.productSolde[i] != '+' :
                self.productSolde = self.productSolde[:i]
                break
        self.productShipping = True if self.productShipping != "" else False
        self.productPrice = self.productPrice.split('D')[1] if self.productPrice else ""
        self.productOldPrice = self.productOldPrice.split('D')[1] if self.productOldPrice else ""


    def printProduct(self):
        print()
        print("--------------------------")
        print(f"Title : {self.productTitle}")
        print(f"Solde : {self.productSolde}")
        print(f"Review Rate : {self.productRevRate}")
        print(f"Shipping : {self.productShipping}")
        print(f"Price : {self.productPrice}")
        print(f"Old Price : {self.productOldPrice}")
        print("--------------------------")