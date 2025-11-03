from django.urls import path
from . import views


urlpatterns = [
     path('register/', views.register_page, name='register_page'),
    path('login/', views.login_page, name='login_page'),
    path('logout/', views.logout_page, name='logout_page'),



    path("register/", views.register, name="register"),   
    path("login/", views.login_view, name="login_view"),        
    path("logout/", views.logout, name="logout"),      
    path("me/", views.me, name="me"),  
    path("change_password/", views.change_password, name="change_password")
]