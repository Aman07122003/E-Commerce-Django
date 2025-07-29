from .cart import Cart


def cart(request):
    """
    Context processor to add the cart to the context.
    This allows the cart to be accessed in templates without needing to pass it explicitly.
    """
    return {'cart': Cart(request)}