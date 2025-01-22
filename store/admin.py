from django.contrib import admin
from .models import Book, Author, PublishingHouse, Category, Order, OrderItem, Cart, CartItem, ImageOfWebSite, Genre

# Register your models here.
admin.site.register(Author)
admin.site.register(PublishingHouse)
admin.site.register(Category)
admin.site.register(ImageOfWebSite)
admin.site.register(Genre)

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_quantity', 'total_price')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'total_quantity', 'total_price', 'status')

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('book_name', 'author_name', 'isbn', 'page', 'price')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('book', 'quantity', 'total_price')

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('book', 'quantity', 'total_price')
