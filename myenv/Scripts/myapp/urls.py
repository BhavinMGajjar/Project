
from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.index, name='index'),
    path('product', views.product, name='product'),
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
    path('profile', views.profile, name='profile')

]