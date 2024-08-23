from django.shortcuts import render, get_object_or_404, redirect
from .cart import Cart
from store.models import Product
from django.http import JsonResponse 


# Create your views here.
def cart_summary(request):
    cart = Cart(request)
    total_price = cart.get_total_price()
    total_quantity = cart.get_total_quantity()
    return render(request, "cart_summary.html", {'cart': cart, 'total_price': total_price, 'total_quantity': total_quantity})




def cart_add(request):
    cart = Cart(request)
    product_id = request.POST.get('product_id')
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product)
    
    
    
    return redirect('cart_summary')



def cart_update(request):
    cart = Cart(request)
    product_id = request.POST.get('product_id')
    action = request.POST.get('action')

    if action == 'increase':
        cart.add(product=get_object_or_404(Product, id=product_id))
    elif action == 'decrease':
        cart.remove(product=get_object_or_404(Product, id=product_id))
    
    return redirect('cart_summary')


def cart_delete(request):
    cart = Cart(request)
    product_id = request.POST.get('product_id')
    cart.delete(product_id)
    return redirect('cart_summary')