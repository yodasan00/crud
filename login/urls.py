from django.urls import path,include
from . import views
from rest_framework import routers
from django.urls import path
from rest_framework.views import APIView
from rest_framework.response import Response
from .views import CreateOTPView, VerifyOTPView




router=routers.DefaultRouter()
router.register('userDet',views.UserDetailsSerializerViewset)
router.register('licenseDet',views.LicenseDetailsSerializerViewset) 
router.register('users',views.UserViewSet)
urlpatterns = [
    path('login/',views.login_user,name='login'),
    path('user/', views.User_page, name='users'),
    path('', include(router.urls)),
    path('otp/create/', CreateOTPView.as_view(), name='create-otp'),
    path('otp/verify/', VerifyOTPView.as_view(), name='verify-otp'),


]
