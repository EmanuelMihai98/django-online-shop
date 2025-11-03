from django.contrib.auth import authenticate, login, logout as auth_logout
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages

from accounts.serializer import (
    UserSerializer,
    RegisterSerializer,
    LoginSerializer,
    ChangePasswordSerializer,
)


@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    
    login(request, user)
    return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = authenticate(
        request,
        username=serializer.validated_data["username"],
        password=serializer.validated_data["password"],
    )
    if not user:
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

    login(request, user)
    return Response(UserSerializer(user).data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    auth_logout(request)
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
    return Response(UserSerializer(request.user).data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def change_password(request):
    serializer = ChangePasswordSerializer(
        data=request.data,
        context={"request": request},
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({"detail": "Password updated"}, status=status.HTTP_200_OK)


def register_page(request):
    if request.method == 'POST':
    
        form = UserCreationForm(request.POST)
        if form.is_valid():
           
            user = form.save()
           
            login(request, user)
            messages.success(request, f"Your account has been created ->{user.username}")
          
            return redirect('products_list_page') 
        
        else:
            
            messages.error(request, "try again")
    else:
        
        form = UserCreationForm()
        
    context = {'form': form}
    return render(request, 'accounts/register.html', context)


def login_page(request):
    if request.method == 'POST':
        
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
        
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
           
            user = authenticate(username=username, password=password)
            
            if user is not None:
               
                login(request, user)
                messages.info(request, f"Hello {username}.")
             
                return redirect('products_list_page')
            
            else:
                
                messages.error(request, "Incorect credentials")
        else:
         
            messages.error(request, "Incorect credentials")
    else:
     
        form = AuthenticationForm()
        
    context = {'form': form}
    return render(request, 'accounts/login.html', context)


def logout_page(request):
   
    logout(request)
    messages.info(request, "successfully logged out")
   
    return redirect('products_list_page')