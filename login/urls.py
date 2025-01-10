from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.login_user,name='login'),
     path('user/', views.User_page, name='users'),
    
]
