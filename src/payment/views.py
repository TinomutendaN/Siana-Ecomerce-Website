from django.shortcuts import render, redirect
from .forms import ShippingForm
from .models import ShippingAddress, Order
from cart.cart import Cart  # Ensure the cart is imported

def checkout(request):
    cart = Cart(request)  # Create a cart instance
    total_price = cart.get_total_price()  # Calculate total price from the cart
    shipping_cost = 0

    # Determine shipping cost based on total price
    if total_price < 200:
        shipping_cost = total_price * 0.05  # 5% of total price

    if request.method == "POST":
        form = ShippingForm(request.POST)
        if form.is_valid():
            shipping_address = form.save(commit=False)
            if request.user.is_authenticated:
                shipping_address.user = request.user
            shipping_address.save()

            # Create an Order
            total_amount = total_price + shipping_cost
            order = Order(
                user=request.user if request.user.is_authenticated else None,
                first_name=shipping_address.full_name.split()[0],
                last_name=' '.join(shipping_address.full_name.split()[1:]),
                email=shipping_address.email,
                address=shipping_address.address1,
                city=shipping_address.city,
                country=shipping_address.country,
                zipcode=shipping_address.zipcode,
                telephone=shipping_address.telephone,
                shipping_cost=shipping_cost,
                total=total_amount
            )
            order.save()

            # Clear the cart
            request.session.pop('session_key', None)

            # Redirect to payment success page after order creation
            return redirect('payment_success')
    else:
        form = ShippingForm()

    return render(request, "payment/checkout.html", {
        "form": form,
        "cart": cart,
        "total_price": total_price,
        "shipping_cost": shipping_cost,
        "grand_total": total_price + shipping_cost
    })

def payment_success(request):
    return render(request, "payment/payment_success.html", {})

def terms(request):
    return render(request, "payment/terms.html", {})
