from django.urls import path, include
from . import views

urlpatterns = [
    path("login", views.login_view, name = "login"),
    path("signUp", views.signUp_view, name = "signUp"),
    path("logout", views.logout_view, name = "logout"),

]