from django.shortcuts import render, redirect, get_object_or_404
from django.db import models
from .models import Product, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages 
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django import forms 
import random
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import JsonResponse

# Create your views here.
def index(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'index.html', {'products': products, 'categories': categories})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username= username, password = password)
        if user is not None:
            login(request, user)
            messages.success(request, ("You have been logged In!"))
            return redirect('index')

        else:
            messages.success(request, ("Incorrect Password or username, please try again....."))
            return redirect('login')
    else :
       
       return render(request, 'login.html',{})

def logout_user(request):
    logout(request)
    messages.success(request,("You have been logged out...."))
    return redirect('index')

def register_user(request):
       form = SignUpForm()
       if request.method == "POST":
           form = SignUpForm(request.POST)
           if form.is_valid():
               form.save()
               username = form.cleaned_data['username']
               password = form.cleaned_data['password1']

               # login user
               user = authenticate(username=username, password=password)
               login(request, user)
               messages.success(request,("You have registered successfully !!!"))
               return redirect('index')
           else:
               messages.success(request,("Oops there was a problem registering, please try again later"))
               return redirect('register')

       else:
            return render(request, 'register.html',{'form':form})
       



def product(request, pk):
    try:
        product = Product.objects.get(id=pk)
        related_products = Product.objects.filter(category=product.category).exclude(id=pk)[:4]  # Get related products, limit to 4
        return render(request, 'product.html', {'product': product, 'related_products': related_products})
    except Product.DoesNotExist:
        return redirect('index')  # Redirect if the product doesn't exist
    


def category(request, foo):
    try:
        # Look up the category using the slug
        category = Category.objects.get(slug=foo)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products': products, 'category': category})
    except Category.DoesNotExist:
        return redirect('index')  # Redirect to the homepage if the category doesn't exist


def store(request, category_slug=None):
    # Annotate categories with the count of products in each category
    categories = Category.objects.annotate(product_count=Count('product'))
    
    # Get the selected category IDs from the GET parameters
    selected_categories = request.GET.getlist('category')
    
    # Start with all products
    products = Product.objects.all()

    if selected_categories:
        # Filter products by the selected categories
        products = products.filter(category__id__in=selected_categories)

    # Set up pagination: 12 products per page
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Fetch all products that are on sale
    on_sale_products = Product.objects.filter(is_sale=True)
    
    # Randomly select up to 3 products that are on sale
    top_selling_products = random.sample(list(on_sale_products), min(len(on_sale_products), 3))
    
    return render(request, 'store.html', {
        'categories': categories,
        'top_selling_products': top_selling_products,
        'page_obj': page_obj,
        'selected_categories': selected_categories,
    })

def search(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()
    
    return render(request, "search.html", {'products': products})


