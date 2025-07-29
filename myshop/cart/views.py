from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from django.http import HttpResponse

# Create your views here.
@require_POST
def cart_add(request, product_id):
    """
    Add a product to the cart.
    This view expects a POST request with the product ID and optionally the quantity.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    print("POST data:", request.POST)
    print("Form valid?", form.is_valid())
    print(form.errors)


    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], override_quantity=cd['override'])
    
    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, product_id):
    """
    Remove a product from the cart.
    This view expects a POST request with the product ID.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id, available=True)
    cart.remove(product)

    return redirect('cart:cart_detail')

def cart_detail(request):
    """
    Display the cart details.
    This view renders the cart contents and allows for quantity updates.
    """
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})

def product_detail(request, id, slug):
    """
    Display the details of a specific product.
    This view is used to show product information and allow adding it to the cart.
    """
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()

    return render(request, 'shop/product/detail.html', {
        'product': product,
        'cart_product_form': cart_product_form
    })