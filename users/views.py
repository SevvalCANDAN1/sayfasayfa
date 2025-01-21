from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
# Create your views here.

def user(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    return render(request, "users/user.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("user"))
        else:
            return render(request, "users/login.html", {
                "message": "Yanlış Kullanıcı Adı Veya Şifre!\nTekrar Deneyiniz."
            })
    
    return render(request, "users/login.html")

def signUp_view(request):
    if request.method == "POST":  
        username = request.POST["username"]
        first = request.POST["fname"]
        last = request.POST["lname"]
        mail = request.POST["mail"]
        password = request.POST["password"]
        User.objects.create_user(
            username=username, 
            first_name=first, 
            last_name=last, 
            email=mail, 
            password=password
        )
        return HttpResponseRedirect(reverse("login"))
    return render(request, "users/signUp.html")

def logout_view(request):
    logout(request)
    return render(request, "users/login.html", {
        "message":"Çıkış Yapıldı"
    })
