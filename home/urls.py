from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.Login, name='login'),
    path("register/", views.Register, name='register'),
    path("", views.Home, name='home'),
    path("quote/", views.Quote, name='quote'),
    path("buy/", views.Buy, name='buy'),
    path("sell/", views.Sell, name='sell'),
    path("history/", views.Historys, name='history'),
    path("logout/", views.Logout, name='logout'),
]
