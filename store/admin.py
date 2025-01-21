from django.contrib import admin
from .models import Book, Author, PublishingHouse, Category, Order, OrderItem, Cart, CartItem, ImageOfWebSite, Genre

# Register your models here.
admin.site.register(Book)
admin.site.register(Author)
admin.site.register(PublishingHouse)
admin.site.register(Order)
admin.site.register(Category)
admin.site.register(OrderItem)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(ImageOfWebSite)
admin.site.register(Genre)

