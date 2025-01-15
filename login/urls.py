from django.urls import path,include
from . import views
from rest_framework import routers

router=routers.DefaultRouter()
router.register('userDet',views.UserDetailsSerializerViewset)
router.register('licenseDet',views.LicenseDetailsSerializerViewset) 
router.register('users',views.UserViewSet)
urlpatterns = [
    path('login/',views.login_user,name='login'),
    path('user/', views.User_page, name='users'),
    path('', include(router.urls)),
]
