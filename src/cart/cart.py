from store.models import Product
import logging

logger = logging.getLogger(__name__)

class Cart():
    def __init__(self, request):
        self.session = request.session

        # Get the current session key if it exists
        cart = self.session.get('session_key')

        # If the user is new, no session key! Create one!
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        # Make sure Cart is available on all pages of the site
        self.cart = cart

    def add(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            if 'quantity' not in self.cart[product_id]:
                # Log this unexpected state
                logger.warning(f"Quantity key missing for product_id {product_id}")
                self.cart[product_id]['quantity'] = 1  # Reinitialize if missing
            else:
                self.cart[product_id]['quantity'] += 1
        else:
            self.cart[product_id] = {
                'price': str(product.price),
                'quantity': 1,
                'name': product.name
            }
        self.save()

    def save(self):
        self.session.modified = True

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            # Ensure that 'quantity' is present
            if 'quantity' not in item:
                item['quantity'] = 1
                logger.warning(f"Quantity key missing in item {item}, reinitialized to 1")
            item['total_price'] = float(item['price']) * item['quantity']
            yield item

    def get_total_price(self):
        return sum(float(item['price']) * item['quantity'] for item in self.cart.values())
    
    def get_total_quantity(self):
        return sum(item['quantity'] for item in self.cart.values())
