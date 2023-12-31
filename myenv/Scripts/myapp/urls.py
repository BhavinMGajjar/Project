
from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.index, name='index'),
    path('seller-index', views.seller_index, name='seller-index'),
    path('product/<str:cat>/', views.product, name='product'),
    path('shopping-cart', views.shopping_cart, name='shopping-cart'),
    path('about', views.about, name='about'),
    path('blog', views.blog, name='blog'),
    path('contact', views.contact, name='contact'),
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('forgot-password', views.forgot_password, name='forgot-password'),
    path('verify-otp', views.verify_otp, name='verify-otp'),
    path('new-password', views.new_password, name='new_password'),
    path('logout', views.logout, name='logout'),
    path('profile', views.profile, name='profile'),
    path('change-password', views.change_password, name='change-password'),
    path('seller-add-product', views.seller_add_product, name='seller-add-product'),
    path('seller-view-product', views.seller_view_product, name='seller-view-product'),
    path('seller-product-detail/<int:pk>/', views.seller_product_detail, name='seller-product-detail'),
    path('seller-product-edit/<int:pk>/', views.seller_product_edit, name='seller-product-edit'),
    path('seller-product-delete/<int:pk>/', views.seller_product_delete, name='seller-product-delete'),
    path('product-details/<int:pk>/', views.product_details, name='product-details'),
    path('add-to-wishlist/<int:pk>/', views.add_to_wishlist, name='add-to-wishlist'),
    path('wishlist', views.wishlist, name='wishlist'),
    path('remove-from-wishlist/<int:pk>/', views.remove_from_wishlist, name='remove-from-wishlist')
]