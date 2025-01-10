from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
def login_user(request):
    if request.method == "POST":
        license = request.POST["licence"]
        password = request.POST["password"]
        user = authenticate(request, username=license, password=password)
        if user is not None:
            login(request, user)
            return render(request,"registration/sucessful.html")
        else:
            messages.error(request, "Enter correct details ;-(")
            return render(request, 'registration/log.html')
    else:
        return render(request, 'registration/log.html')
    
@login_required

def User_page(request):
    return render(request,"registration/sucessful.html")