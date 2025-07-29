from decimal import Decimal
from django.conf import settings
from shop.models import Product

class Cart:
    def __init__(self, request):
        """
        Initialize the cart with the request session.
        The cart is stored in the session under the key defined by CART_SESSION_ID.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            # If the cart does not exist, create an empty cart
            cart = self.session[settings.CART_SESSION_ID] = {}
            self.session.modified = True
        self.cart = cart


    def add(self, product, quantity=1, override_quantity=False):
        """
        Add a product to the cart or update its quantity.
        If the product is already in the cart, update its quantity.
        If override_quantity is True, set the quantity to the specified amount.
        """
        product_id = str(product.id)
        print("Adding product {product_id} to cart with quantity {quantity} and override {override_quantity}")

        if product_id not in self.cart:
            # If the product is not in the cart, add it
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}

        if override_quantity:
            # If overriding quantity, set it directly
            self.cart[product_id]['quantity'] = quantity
        else:
            # Otherwise, increment the quantity
            self.cart[product_id]['quantity'] += quantity

        self.session.modified = True

        self.save()

    def save(self):
        """
        This method is called after any modification to the cart.
        """
        self.session.modified = True


    def remove(self, product):
        """
        Remove a product from the cart.
        """
        product_id = str(product.id)

        if product_id in self.cart:
            del self.cart[product_id]
            self.save()


    def __iter__(self):
        """
        Iterate over the items in the cart and yield each product with its details.
        """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item


    def __len__(self):
        """
        Count the total number of items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())
    

    def get_total_price(self):
        """
        Calculate the total price of all items in the cart.
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
    
    def clear(self):
        """
        Clear the cart by removing it from the session.
        """
        del self.session[settings.CART_SESSION_ID]
        self.save()

