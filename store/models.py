from django.db import models
import datetime
from django.contrib.auth.models import User

# Create your models here.

#Category modeli kitabın türlerini içerir. Ör: masal, hikaye...
class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name
    
class PublishingHouse(models.Model):
    name = models.CharField(max_length=64)
    photo = models.ImageField(upload_to='publishing_house_photo/')

    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=64)
    information = models.CharField(max_length=6000)
    photo = models.ImageField(upload_to='author_photos/')

    def __str__(self):
        return f"{self.name} "


class Genre(models.Model):
    name  = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
#All of Books
class Book(models.Model):
    book_name = models.CharField(max_length=64)
    author_name = models.ForeignKey(Author, on_delete=models.CASCADE, related_name = 'books')
    publication_date = models.DateTimeField()
    publishing_house = models.ForeignKey(PublishingHouse, on_delete = models.CASCADE, related_name = 'books')
    category = models.ManyToManyField(Category, related_name = 'books')
    isbn = models.BigIntegerField()
    page = models.IntegerField()
    price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    photo = models.ImageField(upload_to='books_photos/')
    info = models.CharField(max_length=6000)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name= 'books', default = 4)
    def __str__(self):
        return f"{self.book_name} "

class Cart(models.Model):
    user =  models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    books = models.ManyToManyField(Book, through='CartItem')
    total_quantity = models.IntegerField(default=0) #Sepetteki kitap sayısı
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default= 0.0)


    def __Str__(self):
        return f" Cart of {self.user.username}"

    
    def save(self,*args, **kwargs):
        '''Sepetteki toplam sayıyı ve fiyatı günceller'''
        if self.pk:  # Eğer birincil anahtar varsa (nesne kaydedildiyse)
            self.total_quantity = sum(item.quantity for item in self.cart_items.all())
            self.total_price = sum(item.total_price for item in self.cart_items.all())
        super().save(*args, **kwargs)
        



class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='cart_items', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, related_name='cart_items', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places = 2, default= 0.0)

    def __str__(self):
        return f"{self.quantity} of {self.book.book_name}"
    
    def save(self, *args, **kwargs):
        '''Toplam fiyatı güncelle'''
        self.total_price = self.quantity * self.book.price
        super().save(*args, **kwargs)

    def delete_book(self, *args, **kwargs):
        self.quantity -=1
        self.save()
    
class OrderItem(models.Model):
    book = models.ForeignKey(Book, related_name='order_items',  on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default = 0.0)

    def __str__(self):
        return f"{self.quantity} of {self.book.book_name} "
    
    def save(self, *args, **kwargs):
        """Toplam fiyatı güncelle"""
        self.total_price = self.quantity * self.book.price
        super().save(*args, **kwargs)

class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE,  null=True, blank=True)
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=1000, default='No address provided')
    phone = models.CharField(max_length=20, default='', blank=True)
    date = models.DateField(default=datetime.datetime.today)
    c_name = models.CharField(max_length=30, default='')
    c_num = models.IntegerField(default=1)
    cvc = models.IntegerField(default=1)
    status = models.BooleanField(default=False)
    total_quantity = models.IntegerField(default=0) #Sepetteki kitap sayısı
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default= 0.0)
    order_items = models.ManyToManyField(OrderItem, related_name = 'order_items')

    def __str__(self):
        return f"Order {self.id} by {self.customer.username}"
    
    @classmethod
    def create_order_from_cart(cls, cart):
        if not cart:
            raise ValueError("Geçerli bir sepet bulunamadı veya sepet boş.")

        # Sipariş oluştur
        order = cls(
            customer=cart.user,
            total_quantity=cart.total_quantity,
            total_price=cart.total_price
        )
        order.save()

        # Sepet öğelerini sipariş öğelerine dönüştür
        for item in cart.cart_items.all():
            order_item = OrderItem.objects.create(
                book=item.book,
                quantity=item.quantity,
                total_price=item.total_price
            )
            order.order_items.add(order_item)

        # Sepeti boşalt
        cart.cart_items.all().delete()
        return order



class ImageOfWebSite(models.Model):
    name = models.CharField(max_length=64)
    photo = models.ImageField(upload_to='website_photos/')

    def __str__(self):
        return f"{self. name} photo : {self.photo}"

