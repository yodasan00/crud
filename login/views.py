from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from.serializers import UserDetailsSerializer,LicenseDetailsSerializer,userSerializer
from .models import UserDetails,LicenseDetails
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import User


def login_user(request):
    if request.method == "POST":
        license = request.POST["licence"]
        password = request.POST["password"]
        
        # Check if the username exists
        if not User.objects.filter(username=license).exists():
            messages.error(request, "Username is incorrect. Please try again.")
            return render(request, 'registration/log.html')
        
        # Authenticate the user
        user = authenticate(request, username=license, password=password)
        if user is not None:
            login(request, user)
            return render(request, "registration/sucessful.html")
        else:
            messages.error(request, "Password is incorrect. Please try again.")
            return render(request, 'registration/log.html')
    else:
        return render(request, 'registration/log.html')

@login_required

def User_page(request):
    return render(request,"registration/sucessful.html")

class UserDetailsSerializerViewset(viewsets.ModelViewSet):
    serializer_class = UserDetailsSerializer
    queryset = UserDetails.objects.all()
    authentication_classes=(TokenAuthentication,)

class LicenseDetailsSerializerViewset( viewsets.ModelViewSet):
    serializer_class = LicenseDetailsSerializer
    queryset = LicenseDetails.objects.all()
    authentication_classes=(TokenAuthentication,)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = userSerializer
   