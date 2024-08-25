from .cart import Cart
from store.models import Category

# Create context processor so that our cart works on all pages

def cart(request):
    # Initialize the cart
    cart = Cart(request)
    
    # Calculate the total quantity of items in the cart
    total_quantity = cart.get_total_quantity()
    
    # Calculate the total price of items in the cart
    total_price = cart.get_total_price()
    
    # Return the cart, total quantity, and total price to be accessible in all templates
    return {
        'cart': cart,
        'total_quantity': total_quantity,
        'total_price': total_price,
    }

def category_processor(request):
    return {
        'categories': Category.objects.all()
    }



