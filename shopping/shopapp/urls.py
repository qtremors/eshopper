"""
URL configuration for shopping project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .import views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),

    path('contact', views.contact, name='contact'),
    path('shop', views.shop, name='shop'),
    path('detail', views.detail, name='detail'),

    path('cart', views.cart, name='cart'),
    path('order', views.order, name='order'),
    path('checkout', views.checkout, name='checkout'),
    path('apply_coupon/', views.apply_coupon, name='apply_coupon'),
    path('cancel_order/<int:id>/', views.cancel_order, name='cancel_order'),
    
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('inc_product/<int:id>/', views.inc_product, name='inc_product'),
    path('dec_product/<int:id>/', views.dec_product, name='dec_product'),
    path('del_product/<int:id>/', views.del_product, name='del_product'),

    path('wishlist/', views.wishlist, name='wishlist'),
    path('add_to_wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove_from_wishlist/<int:id>/', views.del_wishlist_product, name='del_wishlist_product'),

    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('profile', views.profile, name='profile'),
    path('update_profile', views.update_profile, name='update_profile'),
    path('register', views.register, name='register'),
    path('forget/', views.forget, name='forget'),
    path('confirm_password/', views.confirm_password, name='confirm_password'),

    path('shop/<str:subcategory_name>/', views.shop, name='shop_by_subcategory'),

    path('detail/<int:id>', views.detail, name='detail'),
    path('add_review/<int:product_id>/', views.add_review, name='add_review'),
    path('detail/<int:product_id>/add_review/', views.add_review, name='add_review')
]
