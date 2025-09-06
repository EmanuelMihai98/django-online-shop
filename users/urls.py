from django.urls import path
from . import views


urlpatterns = [
    path("register/", views.register, name="register"),   
    path("login/", views.login_view, name="login_view"),        
    path("logout/", views.logout, name="logout"),      
    path("me/", views.me, name="me"),  
    path("change_password/", views.change_password, name="change_password")
]