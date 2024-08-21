from .cart import Cart

# Create context processor so that our cart works on all pages

def cart(request):
    # Return the default data from our cart

    cart = Cart(request)
    total_quantity = cart.get_total_quantity()
    return {'cart': cart, 'total_quantity': total_quantity}