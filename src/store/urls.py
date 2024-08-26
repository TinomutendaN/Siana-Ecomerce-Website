from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name = "index"),
    path("login/", views.login_user, name = "login"),
    path("logout/", views.logout_user, name = "logout"),
    path("register/", views.register_user, name = "register"),
    path("product/<int:pk>/", views.product, name="product"),
    path("category/<str:foo>/", views.category, name = "category"),
    path("store/", views.store, name = "store"),
    path('store/category/<slug:category_slug>/', views.store, name='products_by_category'),
    path("search/", views.search, name = "search"),
    path("about/", views.about, name="about"),
   
    
   ]