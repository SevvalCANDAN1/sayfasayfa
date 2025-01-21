from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('book/<int:id>/', views.book_page, name = 'book_page'),
    path('category/<str:name>/', views.category_page, name = 'category_page'),
    path('author/<str:name>/', views.author_page, name = 'author_page'),
    path('publishing_house/<str:name>/', views.publishing_house_page, name = 'publishing_house_page'),
    path('genre/<str:name>/', views.genre_page, name = 'genre_page'),
    path('cart/', views.cart_page, name = 'cart_page'),
    path('authors/', views.authors_page, name = 'authors_page'),
    path('publishing_houses/', views.publishing_houses_page, name = 'publishing_houses_page'),
    path('login', views.login_view, name = "login"),
    path("signUp", views.signUp_view, name = "signUp"),
    path("logout", views.logout_view, name = "logout"),
    path('users/', views.user_store, name = 'user'),
    path('add_to_cart/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('delete/<int:book_id>/', views.delete_to_cart, name="delete_to_cart"),
    path('siparis/', views.order, name='order'),
    path('arama/', views.search, name="search")
    

    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)