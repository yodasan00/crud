from django.urls import path,include
from . import views
from rest_framework import routers
from django.urls import path
from rest_framework.views import APIView
from rest_framework.response import Response
from .views import CreateOTPView, VerifyOTPView,  LicenseDetailsSerializerViewset, MGQDetailsViewSet, AddressDetailsViewSet,UnitDetailsViewSet,MemberDetailViewSet




router=routers.DefaultRouter()
router.register('users',views.UserViewSet)
router.register('user-det',views.UserDetailsSerializerViewset)
router.register('license-det',LicenseDetailsSerializerViewset) 
router.register('mgq-details', MGQDetailsViewSet)
router.register('address-details', AddressDetailsViewSet)
router.register('unit-details', UnitDetailsViewSet)
router.register('member-details', MemberDetailViewSet)
urlpatterns = [
    path('login/',views.login_user,name='login'),
    path('otp/create/', CreateOTPView.as_view(), name='create-otp'),
    path('otp/verify/', VerifyOTPView.as_view(), name='verify-otp'),

    path('', include(router.urls)),
 

]
