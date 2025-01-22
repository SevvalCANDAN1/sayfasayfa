from django.shortcuts import render, get_object_or_404
from . models import  Book, Category, ImageOfWebSite, Author, PublishingHouse, Genre, Cart, CartItem, Order, OrderItem
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime

# Create your views here.
def add_to_cart(request, book_id):
    if not request.user.is_authenticated:
        messages.warning(request, "Sepetinize Ürün Eklemek İçin Giriş Yapmanız Gerekmektedir! İyi alışverişler...")
        return redirect('login')
    
    book = get_object_or_404(Book, id=book_id)
    
    # Kullanıcının aktif sepetini kontrol et veya oluştur
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Sepette bu kitabı kontrol et
    cart_item, created = CartItem.objects.get_or_create(cart=cart, book=book)
    
    if not created:  # Eğer zaten varsa, miktarı artır
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, f"{book.book_name} sepete eklendi. (Miktar: {cart_item.quantity})")
    else:
        messages.success(request, f"{book.book_name} sepete eklendi.")
    cart.save()
    return redirect('cart_page')

def delete_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    cart = get_object_or_404(Cart, user=request.user)

    #Sepette kitap var mı yok mu
    cart_item = CartItem.objects.filter(cart=cart, book=book).first()


    if cart_item:
        if cart_item.quantity > 1:
            cart_item.delete_book()
            messages.success(request, f"{book.book_name} sepetten çıkarıldı. (Kalan miktar: {cart_item.quantity})")
        else:
            cart_item.delete()
            messages.success(request, f"{book.book_name} sepetten tamamen kaldırıldı.")

    else:
        messages.error(request, "Bu kitap zaten sepetinizde değil.")
    return redirect('cart_page')


def cart_page(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Sepetinizi Görebilmek İçin Giriş Yapmanız Gerekiyor. İyi alışverişler...")
        return HttpResponseRedirect(reverse("login"))
    else:
        categories = Category.objects.all()
        home_page_photo = ImageOfWebSite.objects.get(name = 'home-page-photo')
        user_icon = ImageOfWebSite.objects.get(name = 'user-icon')
        navigation = ImageOfWebSite.objects.get(name = 'navigation-bar-icon')
        cart = ImageOfWebSite.objects.get(name = 'cart-photo')
        logo = ImageOfWebSite.objects.get(name = 'web-site-logo')
        authors = Author.objects.all()
        publishing_houses = PublishingHouse.objects.all()
        genres = Genre.objects.all()
        cart_user = Cart.objects.filter(user=request.user).first()  # Kullanıcıya ait cart'ı al
        cart_items = cart_user.cart_items.all() if cart_user else [] 
        return render(request, "store/cart.html", {
            'categories': categories,
            'logo' : logo,
            'home_page_photo' : home_page_photo,
            'user_icon' : user_icon,
            'navigation' : navigation,
            'cart' : cart,
            'authors' : authors,
            'publishing_houses' : publishing_houses,
            'genres' : genres,
            'cart_items': cart_items,
            'cart_user': cart_user,
        })

def home(request):
    books = Book.objects.all()[:16]
    categories = Category.objects.all()
    home_page_photo = ImageOfWebSite.objects.get(name = 'home-page-photo')
    user_icon = ImageOfWebSite.objects.get(name = 'user-icon')
    navigation = ImageOfWebSite.objects.get(name = 'navigation-bar-icon')
    cart = ImageOfWebSite.objects.get(name = 'cart-photo')
    logo = ImageOfWebSite.objects.get(name = 'web-site-logo')
    authors = Author.objects.all()
    publishing_houses = PublishingHouse.objects.all()
    genres = Genre.objects.all()
    return render(request, 'store/index.html', 
                  {'books':books, 
                   'categories' : categories,
                    'logo' : logo,
                    'home_page_photo' : home_page_photo,
                    'user_icon' : user_icon,
                    'navigation' : navigation,
                    'cart' : cart,
                    'authors' : authors,
                    'publishing_houses' : publishing_houses,
                    'genres' : genres,
                   })

def book_page(request, id):
    book = get_object_or_404(Book, id = id)
    categories_of_book = book.category.all()[0]
    category_name = categories_of_book
    author = book.author_name
    books = Book.objects.filter(category = category_name)[:4]
    categories = Category.objects.all()
    home_page_photo = ImageOfWebSite.objects.get(name = 'home-page-photo')
    user_icon = ImageOfWebSite.objects.get(name = 'user-icon')
    navigation = ImageOfWebSite.objects.get(name = 'navigation-bar-icon')
    cart = ImageOfWebSite.objects.get(name = 'cart-photo')
    logo = ImageOfWebSite.objects.get(name = 'web-site-logo')
    authors = Author.objects.all()
    publishing_houses = PublishingHouse.objects.all()
    genres = Genre.objects.all()
    return render(request, 'store/book_page.html', {
        'book': book, 
        'categories' : categories, 
        'books': books,
        'logo' : logo,
        'home_page_photo' : home_page_photo,
        'user_icon' : user_icon,
        'navigation' : navigation,
        'cart' : cart,
        'authors' : authors,
        'publishing_houses' : publishing_houses,
        'genres' : genres,
        })

def category_page(request, name):
    category_name = get_object_or_404(Category, name = name)
    categories = Category.objects.filter()  # Kategorileri alın
    books = Book.objects.filter(category=category_name)
    home_page_photo = ImageOfWebSite.objects.get(name = 'home-page-photo')
    user_icon = ImageOfWebSite.objects.get(name = 'user-icon')
    navigation = ImageOfWebSite.objects.get(name = 'navigation-bar-icon')
    cart = ImageOfWebSite.objects.get(name = 'cart-photo')
    logo = ImageOfWebSite.objects.get(name = 'web-site-logo')
    authors = Author.objects.all()
    publishing_houses = PublishingHouse.objects.all()
    genres = Genre.objects.all()
    return render(request, 'store/category_page.html', {
        'logo' : logo,
        'home_page_photo' : home_page_photo,
        'user_icon' : user_icon,
        'navigation' : navigation,
        'category': category_name, 
        'categories': categories, 
        'books':books,
        'cart' : cart,
        'authors' : authors,
        'publishing_houses' : publishing_houses,
        'genres' : genres,
        })
def user(request):
    categories = Category.objects.all()
    home_page_photo = ImageOfWebSite.objects.get(name = 'home-page-photo')
    user_icon = ImageOfWebSite.objects.get(name = 'user-icon')
    navigation = ImageOfWebSite.objects.get(name = 'navigation-bar-icon')
    cart = ImageOfWebSite.objects.get(name = 'cart-photo')
    logo = ImageOfWebSite.objects.get(name = 'web-site-logo')
    authors = Author.objects.all()
    publishing_houses = PublishingHouse.objects.all()
    genres = Genre.objects.all()
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"), {
            'logo' : logo,
            'home_page_photo' : home_page_photo,
            'user_icon' : user_icon,
            'navigation' : navigation,
            'cart' : cart,
            'authors' : authors,
            'publishing_houses' : publishing_houses,
            'genres' : genres,
            'categories' : categories,
        })
    user = request.user

    orders = Order.objects.filter(customer=request.user)

    delivered_order = list()  
    undelivered_order = list()
    for order in orders:
        if order.status:
            delivered_order.append(order)
        else: 
            undelivered_order.append(order)
    
    return render(request, "store/user.html", {
        'logo' : logo,
        'home_page_photo' : home_page_photo,
        'user_icon' : user_icon,
        'navigation' : navigation,
        'cart' : cart,
        'authors' : authors,
        'publishing_houses' : publishing_houses,
        'genres' : genres,
        'categories' : categories,
        'user' : user,
        'delivered_order': delivered_order,
        'undelivered_order': undelivered_order,
    })

def login_view(request):
    categories = Category.objects.all()
    home_page_photo = ImageOfWebSite.objects.get(name = 'home-page-photo')
    user_icon = ImageOfWebSite.objects.get(name = 'user-icon')
    navigation = ImageOfWebSite.objects.get(name = 'navigation-bar-icon')
    cart = ImageOfWebSite.objects.get(name = 'cart-photo')
    logo = ImageOfWebSite.objects.get(name = 'web-site-logo')
    authors = Author.objects.all()
    publishing_houses = PublishingHouse.objects.all()
    genres = Genre.objects.all()
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("user"))
        else:
            return render(request, "store/login.html", {
                "message": "Yanlış Kullanıcı Adı Veya Şifre!\nTekrar Deneyiniz.",
                'logo' : logo,
                'home_page_photo' : home_page_photo,
                'user_icon' : user_icon,
                'navigation' : navigation,
                'cart' : cart,
                'authors' : authors,
                'publishing_houses' : publishing_houses,
                'genres' : genres,
                'categories' : categories,
            })
    
    return render(request, "store/login.html", {
        'logo' : logo,
        'home_page_photo' : home_page_photo,
        'user_icon' : user_icon,
        'navigation' : navigation,
        'cart' : cart,
        'authors' : authors,
        'publishing_houses' : publishing_houses,
        'genres' : genres,
        'categories' : categories,

    })

def order(request):
    categories = Category.objects.all()
    home_page_photo = ImageOfWebSite.objects.get(name = 'home-page-photo')
    user_icon = ImageOfWebSite.objects.get(name = 'user-icon')
    navigation = ImageOfWebSite.objects.get(name = 'navigation-bar-icon')
    cart = ImageOfWebSite.objects.get(name = 'cart-photo')
    logo = ImageOfWebSite.objects.get(name = 'web-site-logo')
    tik = ImageOfWebSite.objects.get(name = 'tik')
    authors = Author.objects.all()
    publishing_houses = PublishingHouse.objects.all()
    genres = Genre.objects.all()
    cart_user = Cart.objects.filter(user=request.user).first()  # Kullanıcıya ait cart'ı al
    cart_items = cart_user.cart_items.all() if cart_user else [] 
    if request.method == "POST":
        if cart_user and cart_items.exists():
            # Siparişi oluştur
            order = Order.create_order_from_cart(cart_user)  # Order nesnesi oluşturuluyor
            

            # Bilgileri siparişe ekle
            order.address = request.POST["adres"]
            order.phone = request.POST["tel"]
            order.c_name = request.POST["cart-name"]
            order.c_num = request.POST["cart-num"]
            order.cvc = request.POST["cvc"]
            order.date = datetime.now()

            # Siparişi kaydet
            order.save()

            messages.success(request, "Siparişiniz başarıyla oluşturuldu!")
            return render(request, "store/order.html", {
                "categories": categories,
                "home_page_photo": home_page_photo,
                "user_icon": user_icon,
                "navigation": navigation,
                "cart": cart,
                "logo": logo,
                "tik": tik,
                "authors": authors,
                "publishing_houses": publishing_houses,
                "genres": genres,
            })
        else:
            messages.warning(request, "Sepetinizde ürün bulunmamaktadır.")
            return render(request, "store/cart.html", {
                "categories": categories,
                "home_page_photo": home_page_photo,
                "user_icon": user_icon,
                "navigation": navigation,
                "cart": cart,
                "logo": logo,
                "tik": tik,
                "authors": authors,
                "publishing_houses": publishing_houses,
                "genres": genres,
            })
            

    

def signUp_view(request):
    categories = Category.objects.all()
    home_page_photo = ImageOfWebSite.objects.get(name = 'home-page-photo')
    user_icon = ImageOfWebSite.objects.get(name = 'user-icon')
    navigation = ImageOfWebSite.objects.get(name = 'navigation-bar-icon')
    cart = ImageOfWebSite.objects.get(name = 'cart-photo')
    logo = ImageOfWebSite.objects.get(name = 'web-site-logo')
    authors = Author.objects.all()
    publishing_houses = PublishingHouse.objects.all()
    genres = Genre.objects.all()
    if request.method == "POST":  
        username = request.POST["username"]
        first = request.POST["fname"]
        last = request.POST["lname"]
        mail = request.POST["mail"]
        password = request.POST["password"]
        if User.objects.filter(username=username).exists():
            messages.error(request, "Bu kullanıcı adı zaten alınmış. Lütfen başka bir kullanıcı adı seçin.")
            return render(request, "store/signUp.html", {
                "categories": categories,
                "home_page_photo": home_page_photo,
                "user_icon": user_icon,
                "navigation": navigation,
                "cart": cart,
                "logo": logo,
                "authors": authors,
                "publishing_houses": publishing_houses,
                "genres": genres
            })
        else:
            User.objects.create_user(
                username=username, 
                first_name=first, 
                last_name=last, 
                email=mail, 
                password=password
            )
            messages.success(request, "Kayıt işlemi başarılı!")
            '''if User.objects.filter(username=username).exists():
                messages.error(request, "Bu kullanıcı adı zaten alınmış. Lütfen başka bir kullanıcı adı seçin.")
            return render(request, "store/signUp.html", {
                "categories": categories,
                "home_page_photo": home_page_photo,
                "user_icon": user_icon,
                "navigation": navigation,
                "cart": cart,
                "logo": logo,
                "authors": authors,
                "publishing_houses": publishing_houses,
                "genres": genres
            })
        User.objects.create_user(
            username=username, 
            first_name=first, 
            last_name=last, 
            email=mail, 
            password=password
        )'''
        return HttpResponseRedirect(reverse("login"), {
            'logo' : logo,
            'home_page_photo' : home_page_photo,
            'user_icon' : user_icon,
            'navigation' : navigation,
            'cart' : cart,
            'authors' : authors,
            'publishing_houses' : publishing_houses,
            'genres' : genres,
            'categories' : categories,
            'user': user,
        })
    return render(request, "store/signUp.html", {
        'logo' : logo,
        'home_page_photo' : home_page_photo,
        'user_icon' : user_icon,
        'navigation' : navigation,
        'cart' : cart,
        'authors' : authors,
        'publishing_houses' : publishing_houses,
        'genres' : genres,
        'categories' : categories,
    })

def logout_view(request):
    categories = Category.objects.all()
    home_page_photo = ImageOfWebSite.objects.get(name = 'home-page-photo')
    user_icon = ImageOfWebSite.objects.get(name = 'user-icon')
    navigation = ImageOfWebSite.objects.get(name = 'navigation-bar-icon')
    cart = ImageOfWebSite.objects.get(name = 'cart-photo')
    logo = ImageOfWebSite.objects.get(name = 'web-site-logo')
    authors = Author.objects.all()
    publishing_houses = PublishingHouse.objects.all()
    genres = Genre.objects.all()
    logout(request)
    return render(request, "store/login.html", {
        "message":"Çıkış Yapıldı", 
        'logo' : logo,
        'home_page_photo' : home_page_photo,
        'user_icon' : user_icon,
        'navigation' : navigation,
        'cart' : cart,
        'authors' : authors,
        'publishing_houses' : publishing_houses,
        'genres' : genres,
        'categories' : categories,
    })

def user_store(request):
    return user(request)

def author_page(request, name):
    author = get_object_or_404(Author, name = name)
    books = Book.objects.filter(author_name=author)
    categories = Category.objects.all()
    home_page_photo = ImageOfWebSite.objects.get(name = 'home-page-photo')
    user_icon = ImageOfWebSite.objects.get(name = 'user-icon')
    navigation = ImageOfWebSite.objects.get(name = 'navigation-bar-icon')
    cart = ImageOfWebSite.objects.get(name = 'cart-photo')
    logo = ImageOfWebSite.objects.get(name = 'web-site-logo')
    authors = Author.objects.all()
    publishing_houses = PublishingHouse.objects.all()
    genres = Genre.objects.all()
    return render(request, 'store/author-page.html', {
        'author': author,
        'books' : books,
        'logo' : logo,
        'home_page_photo' : home_page_photo,
        'user_icon' : user_icon,
        'navigation' : navigation,
        'cart' : cart,
        'authors' : authors,
        'publishing_houses' : publishing_houses,
        'genres' : genres,
        'categories' : categories,
    })

def publishing_house_page(request, name):
    publishing_house1 = get_object_or_404(PublishingHouse, name = name)
    books = Book.objects.filter(publishing_house = publishing_house1)
    categories = Category.objects.all()
    home_page_photo = ImageOfWebSite.objects.get(name = 'home-page-photo')
    user_icon = ImageOfWebSite.objects.get(name = 'user-icon')
    navigation = ImageOfWebSite.objects.get(name = 'navigation-bar-icon')
    cart = ImageOfWebSite.objects.get(name = 'cart-photo')
    logo = ImageOfWebSite.objects.get(name = 'web-site-logo')
    authors = Author.objects.all()
    publishing_houses = PublishingHouse.objects.all()
    genres = Genre.objects.all()
    return render(request, 'store/publishing-house-page.html', {
        'logo' : logo,
        'home_page_photo' : home_page_photo,
        'user_icon' : user_icon,
        'navigation' : navigation,
        'cart' : cart,
        'authors' : authors,
        'publishing_houses' : publishing_houses,
        'genres' : genres,
        'categories' : categories,
        'publishing_house' : publishing_house1,
        'books' : books,
    })

def genre_page(request, name):
    genre1 = get_object_or_404(Genre, name = name)
    books = Book.objects.filter(genre = genre1)
    categories = Category.objects.all()
    home_page_photo = ImageOfWebSite.objects.get(name = 'home-page-photo')
    user_icon = ImageOfWebSite.objects.get(name = 'user-icon')
    navigation = ImageOfWebSite.objects.get(name = 'navigation-bar-icon')
    cart = ImageOfWebSite.objects.get(name = 'cart-photo')
    logo = ImageOfWebSite.objects.get(name = 'web-site-logo')
    authors = Author.objects.all()
    publishing_houses = PublishingHouse.objects.all()
    genres = Genre.objects.all()
    return render(request, 'store/genre-page.html', {
        'genre' : genre1,
        'books' : books,
        'logo' : logo,
        'home_page_photo' : home_page_photo,
        'user_icon' : user_icon,
        'navigation' : navigation,
        'cart' : cart,
        'authors' : authors,
        'publishing_houses' : publishing_houses,
        'genres' : genres,
        'categories' : categories,
    })



def authors_page(request):
    authors = Author.objects.all()
    categories = Category.objects.all()
    home_page_photo = ImageOfWebSite.objects.get(name = 'home-page-photo')
    user_icon = ImageOfWebSite.objects.get(name = 'user-icon')
    navigation = ImageOfWebSite.objects.get(name = 'navigation-bar-icon')
    cart = ImageOfWebSite.objects.get(name = 'cart-photo')
    logo = ImageOfWebSite.objects.get(name = 'web-site-logo')
    authors = Author.objects.all()
    publishing_houses = PublishingHouse.objects.all()
    genres = Genre.objects.all()
    return render(request, "store/authors.html", {
        'authors' : authors,
        'logo' : logo,
        'home_page_photo' : home_page_photo,
        'user_icon' : user_icon,
        'navigation' : navigation,
        'cart' : cart,
        'authors' : authors,
        'publishing_houses' : publishing_houses,
        'genres' : genres,
        'categories' : categories,
    })

def publishing_houses_page(request):
    publishing_houses = PublishingHouse.objects.all()
    categories = Category.objects.all()
    home_page_photo = ImageOfWebSite.objects.get(name = 'home-page-photo')
    user_icon = ImageOfWebSite.objects.get(name = 'user-icon')
    navigation = ImageOfWebSite.objects.get(name = 'navigation-bar-icon')
    cart = ImageOfWebSite.objects.get(name = 'cart-photo')
    logo = ImageOfWebSite.objects.get(name = 'web-site-logo')
    authors = Author.objects.all()
    publishing_houses = PublishingHouse.objects.all()
    genres = Genre.objects.all()
    return render(request, 'store/publishing-houses.html', {
        'publishing_houses' : publishing_houses,
        'logo' : logo,
        'home_page_photo' : home_page_photo,
        'user_icon' : user_icon,
        'navigation' : navigation,
        'cart' : cart,
        'authors' : authors,
        'publishing_houses' : publishing_houses,
        'genres' : genres,
        'categories' : categories,
    })

def search(request):
    word = request.GET.get('word', '')
    searched_books = (Book.objects.filter(book_name__icontains=word) | 
                      Book.objects.filter(info__icontains=word) | 
                      Book.objects.filter(author_name__name__icontains=word) | 
                      Book.objects.filter(publishing_house__name__icontains=word))
    searched_publishing_houses = PublishingHouse.objects.filter(name__icontains=word)
    searched_authors = Author.objects.filter(name__icontains=word)

    categories = Category.objects.all()
    home_page_photo = ImageOfWebSite.objects.get(name = 'home-page-photo')
    user_icon = ImageOfWebSite.objects.get(name = 'user-icon')
    navigation = ImageOfWebSite.objects.get(name = 'navigation-bar-icon')
    cart = ImageOfWebSite.objects.get(name = 'cart-photo')
    logo = ImageOfWebSite.objects.get(name = 'web-site-logo')
    authors = Author.objects.all()
    publishing_houses = PublishingHouse.objects.all()
    genres = Genre.objects.all()
    return render(request, 'store/search-page.html', {
        'logo' : logo,
        'home_page_photo' : home_page_photo,
        'user_icon' : user_icon,
        'navigation' : navigation,
        'cart' : cart,
        'authors' : authors,
        'publishing_houses' : publishing_houses,
        'genres' : genres,
        'categories' : categories,
        'searched_books' : searched_books,
        'searched_publishing_houses' : searched_publishing_houses,
        'searched_authors': searched_authors,
    })

