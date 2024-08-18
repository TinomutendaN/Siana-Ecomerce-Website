from django.shortcuts import render, redirect
from .models import Product, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages 
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django import forms 


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
       

#def product(request,pk):
    #product = Product.objects.get(id=pk)
    #return render(request, 'product.html',{'products':product})

#def product(request, pk):
    #try:
        #product = Product.objects.get(id=pk)
        #return render(request, 'product.html', {'product': product})
    #except Product.DoesNotExist:
        #return redirect('index')  # Redirect to the homepage or an error page if the product doesn't exist


def product(request, pk):
    try:
        product = Product.objects.get(id=pk)
        related_products = Product.objects.filter(category=product.category).exclude(id=pk)[:4]  # Get related products, limit to 4
        return render(request, 'product.html', {'product': product, 'related_products': related_products})
    except Product.DoesNotExist:
        return redirect('index')  # Redirect if the product doesn't exist
    
#def category(request,foo):
    # Replace Hyphens with Spaces
    #foo = foo.replace('-', ' ')
    # Grab the category from the url
    #try:
        # look up the category
        #category = Category.objects.get(name=foo)
        #products = Product.objects.filter(category=category)
        #return render(request, 'category.html', {'products':products, 'category':category})


    #except:
        #return redirect('index')

def category(request, foo):
    # Replace hyphens with spaces to match category names in the database
    foo = foo.replace('-', ' ')
    
    try:
        # Look up the category
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products': products, 'category': category})
    
    except Category.DoesNotExist:
        return redirect('index')  # Redirect to the homepage if the category doesn't exist






